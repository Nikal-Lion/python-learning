import requests
import os
import codecs
import datetime
import time
import sys
import random

url = "https://thispersondoesnotexist.com/image"

downloadPath = ".\\Download"
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
    'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br'
}

def main():
    count = 0
    for num in range(0,20):
        nowTime = datetime.datetime.now()
        now = nowTime.strftime('%Y-%m-%d_%H_%M_%S')

        response = requests.get(url,headers=header )
        # print(response.status_code)
        path = "{}\\{}_{}.jpg".format(downloadPath, now, num)

        if 'content-length' in response.headers:
            print("response content length:{}KB".format(round(float(response.headers['content-length'])/1024,2)))

        if (response.status_code == 200):
            f = codecs.open(path, 'wb')  # 代开一个文件，准备以二进制写入文件
            for chunk in response.iter_content(chunk_size=10240):
                if chunk:
                    f.write(chunk)

            f.flush()  # 将缓冲区的数据立即写入缓冲区，并清空缓冲区
            f.close()
            count+=1
        # time.sleep(0.09)
        print("{} 耗时：{}second".format(path, (datetime.datetime.now()-nowTime).seconds))


    print('{}:catch finished, catch {} files'.format(datetime.datetime.now(), count))

if __name__ == "__main__":
    print("{} begin request".format(datetime.datetime.now()))
    sys.exit(main())