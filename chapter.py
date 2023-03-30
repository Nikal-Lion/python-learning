import sys
import requests
import datetime



host = 'http://www.gdbzkz.com'
books = [
    'douluodalu',
    'kunlunshenggong'
]

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
    'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br'
}

contentStr = '<div id="content" class="showtxt">'
blockEndStr = '<div class="page_chapter">'


def main():
    print("please input books index[ douluodalu:{}, guichuideng:{}]".format(books.index("douluodalu"), books.index("kunlunshenggong")))
    bookIndex = input()
    if (bookIndex > len(books)):
        raise Exception("")

    for num in range(60, 171):
        urlFormated = "{}/{}/{}.html".format(host, books[bookIndex], num)
        r = requests.get(urlFormated, headers=header, stream=True)
        
        if (r.status_code != 200):
            print('请求失败:{}'.format(r.status_code))
            continue

        content = r.content.decode('utf-8')

        beginIndex = content.index(contentStr) + len(contentStr)
        endIndex = content.index(blockEndStr) + 1
        contentBodyLength = endIndex - beginIndex
        print(content[beginIndex: contentBodyLength].replace("&nbsp;"," ").replace("<br />", "\r"))
        break

if __name__ == "__main__":
    print("{} begin request".format(datetime.datetime.now()))
    sys.exit(main())