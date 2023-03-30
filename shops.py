import datetime
import sys
# import importlib
import json
from urllib.request import Request, urlopen
from urllib.parse import quote, unquote
import threading

from numpy import rint
# importlib.reload(sys)

sql_result_path = "data/shop_update.sql"
json_file_path = "data/shops.json"
json_org_path = "data/org.json"
json_abnormal_path = "data/abnormal_shop.json"


def pairs(row):
    # shop = {id: values["ID"], shop_address: values["AREA_NAME_1"] +
    #         values["AREA_NAME_2"] + values["AREA_NAME_3"]}
    # print(shop)
    # if type(values) is list:
    #     print(values[0])
    new_row = tuple()
    for column in row:
        if column[0] == "ID" or column[0] == "AREA_NAME_1":
            return 1

    return row


class Read():

    def read_json(self, json_path):
        # , object_pairs_hook=pairs
        return json.load(open(json_path, 'r', encoding="utf-8"))['shops']

    def write_json(self, json_path, content, mode="a+", indent=4):
        json_file = open(json_path, mode=mode,
                         encoding="utf-8", newline="\r\n")
        json.dump(content, json_file, ensure_ascii=False, indent=indent)
        print(1)


class AmapService():

    api_host = "https://restapi.amap.com"
    api_key = "c6d13c63cd421ddfc1fd09751c1b11cd"

    org_list = []

    def get_location(self, id, org_id, address):
        print("get address:", address)
        api_address = "%s/v3/geocode/geo?key=%s" % (
            self.api_host, self.api_key)
        location = self.api_request(
            "%s&address=%s&city=%s" % (api_address, address, ""))
        return self.save_location(id=id, org_id=org_id, location=location)

    def save_location(self, id, org_id, location):
        """
        保存定位信息

        ``id`` 组织ID，用于更新语句执行的条件

        ``org_id`` 组织编码，用途包含以下功能
        - 更新语句执行的条件
        - 用户中心更新唯一编码

        ``location`` 高德 Api 接口定位返回信息
        """

        location_json = json.loads(location)
        print(location_json, type(location_json))

        geocode = {}
        if location_json["info"] != """OK""":
            print("查询返回值异常: ", location_json)
            return 1
        if str(location_json["count"]) != "1":
            print("查询不止一条记录： %d" % location_json["count"])
            return 1

        geocode = location_json['geocodes'][0]
        if geocode is None:
            print("get id:%d error, response: %s" % (id, str(location)))
            return 1

        location_array = geocode['location'].split(",")
        longitude = location_array[0]
        latitude = location_array[1]
        location_for_db = "%s,%s" % (
            str(location_array[1]), (location_array[0]))

        # print("response location%s" % location_for_db)
        sql = """update Sys_Shop set Location='%s' Where Id=%d and Office_Code='%s';""" % (
            location_for_db, id, org_id)

        org = {"org_id": org_id, "longitude": longitude, "latitude": latitude}
        self.org_list.append(org)

        print("""开始使用追加方式写入文件：""", sql_result_path)
        with open(sql_result_path, mode='a+',
                         encoding="utf-8") as f:
            f.write(sql)

        print("""文件追加写入完成""")

    def api_request(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

        try:
            request = Request(
                url=url, headers=headers, method='GET')

            response = urlopen(request)

            buff = response.read()
            print(buff)
            response = buff.decode('utf8')
            # print("response: %s" % response)
            return response
        except Exception as e:
            print(e)
            return -1

    def save_org_to_json(self):
        json_file = open(json_org_path, mode='a+',
                         encoding="utf-8", newline="\r\n")
        json.dump(self.org_list, json_file, ensure_ascii=False, indent=4)

# print(read)


task_list = list()
api = AmapService()


def get_location_async(id, org_id, address):
    global task_list
    global api
    t = threading.Thread(target=api.get_location,
                         args=(id, org_id, quote(address)))

    if task_list is not None and len(task_list) == 5:
        for task in task_list:
            task.start()
        task_list = []

    task_list.append(t)


def main():
    # sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    # try:
    # api = AmapService()
    # _ = api.get_location(quote("福建省厦门市湖里区鼎丰财富中心", "utf-8"))
    # except Exception as e:
    #     print(e)
    # return 1

    read = Read()
    shops = read.read_json(json_file_path)
    # print(type(shops))

    if shops is None:
        print("Get json content error")
        return 1

    # shop_array = array.array("dict", shops)

    global api
    # shop_list = []
    index = 0
    for item in shops:
        # if index == 6:
        #     break

        print(type(item))
        detail = item.get("COMPANY_ADDRESS", None)

        if detail is None or detail == "" or item.get("SHOP_TYPE", "") == "Purchase":
            json_file = open(json_abnormal_path, mode='a+',
                             encoding="utf-8", newline="\r\n")
            json.dump(item, json_file, ensure_ascii=False, indent=2)
            print("item data does not have area_name", item)
            continue

        # area = item.get("AREA_NAME_1", "") + \
        #     item.get("AREA_NAME_2", "") + item.get("AREA_NAME_3", "")

        # if area is not None and area != "":
        #     detail = detail.replace(area, "")

        get_location_async(item["ID"], item["OFFICE_CODE"], detail)
        # address.append(detail)
        # shop_list.append({id: item["ID"], address: detail})

        # if len(address) == 10:
        #     join_address = '|'.join(address)

        #     address = []
        index += 1

    # if len(address) > 0:
    #     join_address = '|'.join(address)

    #     get_location_async(join_address)
    #     address = []

    # print(address)
    # quoted_address = quote(address, 'utf-8')
    # locations = api.get_location(quoted_address)
    # shop = shops[0]
    # print(shop)
    # area = shop["AREA_NAME_1"] + shop["AREA_NAME_2"] + shop["AREA_NAME_3"]
    # detail = shop["COMPANY_ADDRESS"]

    # if area is not None:
    #     detail = detail.replace(area, "")
    # while shop_array.itemsize > 0:
    # print(1)

    # for shop in shops["shops"]:
    #     print(shop["AREA_NAME_1"])
    if task_list is not None and len(task_list) > 0:
        for task in task_list:
            task.start()
    task_list = []

    api.save_org_to_json()


if __name__ == "__main__":
    print("START AT {}".format(datetime.datetime.now()))
    sys.exit(main())
