import urllib.request
import urllib.parse

url = 'http://www.baidu.com/'
values = {'name':'voidking','language':'Python'}
data = urllib.parse.urlencode(values).encode(encoding='utf-8',errors='ignore')
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

request = urllib.request.Request(url=url,data=data,headers=headers,method='GET')
response = urllib.request.urlopen(request)

buff = response.read()
html = buff.decode('utf8')

print(html)