import threading
import os
import urllib.request
import time


def getImage(res, filePath):
    '''
    :param format: 匹配的正则表达式
    :param url: 获取图片的网址
    :param filePath: 获取的图片存入的文件夹
    :return:
    '''

    time_str = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    path = filePath+"\img"+time_str+"\\"
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    index = 0
    for url in res:
        print(url)
        try:
            f = open(path+str(index)+'.png', 'wb')
            request = urllib.request.urlopen(url)
            buf = request.read()
            f.write(buf)
            index = index + 1
        except Exception:
            continue
        finally:
            #关闭文件
            f.close()


def thread_factory(urls):
    threading.Thread(target=getImage,args=(urls, ""))
