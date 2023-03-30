import datetime
import json
import re
import requests
import chardet
from urllib.parse import quote

from bs4 import BeautifulSoup

# import sys  # 引用sys模块进来，并不是进行sys的第一次加载
# reload(sys)  # 重新加载sys
# sys.setdefaultencoding('utf8')  # 调用setdefaultencoding函数

json_file_path = "data/stone.json"

def get_page_data(url):
    rqg = requests.get(url, headers=headers, timeout=3.0)
    rqg.encoding = chardet.detect(rqg.content)['encoding']  # requests请求过程
    #初始化HTML
    html = rqg.content.decode('utf-8')
    # print(html)
    # return
    soup = BeautifulSoup(html, 'lxml')  # 生成BeautifulSoup对象
    # print("soup object", soup)
    pages = soup.find("a", class_="end").text
    print("total pages", pages)

    pic_boxes = soup.find_all("div", class_="pic_box")
    # print("first div: ", div_content_array[0])
    # print("length of div_content_array: ", len(div_content_array))

    items = []
    for box in pic_boxes:
        # print("enumerate item: ", idx);
        item = translate_html(box)
        items.append(item)
    return items

def translate_html(div_content: any):
    """获取html列表数据"""

    href = div_content.a["href"]
    # print("a.href: ", href)

    img_url = div_content.img["src"]
    replaced_img_url = re.sub(r"\?v=\d+", "", img_url)
    # print("a.img src: ", replaced_img_url)

    item_code = href.split('/')[-1].replace(".html", "")
    # print("item_code", item_code)

    title = div_content.find("p", class_="sc_title").text.replace("石材名称：", "")
    nick_name = div_content.find("p", class_="sc_sort").text.replace(
        "别名：", "").replace("\n", "").replace(" ", "")
    # print("name/nick-name", title, nick_name)
    item = {
        "image": replaced_img_url,
        "item_code": item_code,
        "title": title, 
        "nick_name": nick_name
    }
    return item;

headers = { 
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
    'cache-control': 'no-cache',
    'Refer': 'https://www.stonetmall.com'
    }
cookies = {
    "look_stone_list": "14155%2C15169",
    "phone_code": "137108",
    "phone_code_send_time": "1653297393",
    "pre_page": "",
    "PHPSESSID": "qq89q14nqgv6sevddh36nhfkj5"
}
def main():
    """主方法入口"""
    
    texture = "%E4%B9%B1%E7%BA%B9"
    filters = "" #"/texture/{0}".format(texture)
    # filters += "/color/{1}".format("")
    page = 1
    url_format = "http://www.stonetmall.com/pg/web/stone/index{0}/p/{1}.html"
    url = url_format.format(
        filters, page)
    print("request url: ", url)

    rqg = requests.get(url,cookies=cookies, headers=headers, timeout=3.0)
    rqg.encoding = chardet.detect(rqg.content)['encoding']  # requests请求过程
    #初始化HTML
    html = rqg.content.decode('utf-8')
    # print(html)
    # return 
    soup = BeautifulSoup(html, 'lxml')  # 生成BeautifulSoup对象
    
    # print("soup object", soup)
    total_page = int(soup.find("a",class_="end").text) 
    print("total pages", total_page)

    items = []

    for idx in range(11, total_page):
        print("""开始查询第{}页""".format(idx))
        print("""查询参数：{}""".format(filters))
        url = url_format.format(
            filters, idx)

        
        rqg = requests.get(url, cookies=cookies, headers=headers, timeout=3.0)
        rqg.encoding = chardet.detect(rqg.content)['encoding']  # requests请求过程
        #初始化HTML
        html = rqg.content.decode('utf-8')
        # print(html)
        # return
        soup = BeautifulSoup(html, 'lxml')  # 生成BeautifulSoup对象

        paging_all = soup.find("div", class_="paging_all")
        if(paging_all is None):
            print("""没有更多了""")
            break;

        pic_boxes = soup.find_all("div", class_="pic_box")
        
        for box in pic_boxes:
            # print("enumerate item: ", idx);
            item = translate_html(box)
            items.append(item)
        cookies["pre_page"] = quote(url)

    print("总共获取数据条数：", len(items))

    print("""开始使用追加方式写入文件：""", json_file_path)
    json_file = open(json_file_path, mode='a+', encoding="utf-8")
    json.dump(items, json_file, ensure_ascii=False, indent=4)

    print("""文件追加写入完成""")


if __name__ == "__main__":
    print("{} begin request".format(datetime.datetime.now()))
    main()
