import requests
import os
import codecs
import datetime
import time

url = "https://thispersondoesnotexist.com/image"

path = ".\\Download"
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
    'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br'
}
count = 0
for num in range(1,20):
    now = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
    response = requests.get(url,headers=header )
    print(response.status_code)

    if (response.status_code == 200):
        f = codecs.open("{}\\{}_{}.jpg".format(path, now, num), 'wb')  # 代开一个文件，准备以二进制写入文件
        for chunk in response.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)

        f.flush()  # 将缓冲区的数据立即写入缓冲区，并清空缓冲区
        f.close()
        count+=1
    time.sleep(1)

print('catch finished, catch {} files'.format(count))
exit()