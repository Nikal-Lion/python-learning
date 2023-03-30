import requests
import json
'''发送新增警员信息的http请求'''
#以字典的方式存储需要传递的参数
add_url = 'https://tool.chinaz.com/port/'
search_host = '122.152.201.150'
add_par = {
    'host':'122.152.201.150',
    'port':1
}
#以字典方式储存定制的headers请求头信息
add_header = {
    'Content-Type':'application/json',
    'connection':'keep-alive'
}
#用户登录前的cookies，因为用户登录后才能进行新增警员信息的操作
add_cookie = {
    "JSSESSIONID":"3E2ED9359E53D31FBD13FE2ADE9D20D2"
}
for i in range(1, 65535):
    add_par = {
        "host": search_host,
        "port": i
    }
    r = requests.post(add_url,data=json.dumps(add_par),headers=add_header,cookies=add_cookie)
    #参数要转json格式传输要使用json.dumps()进行转换
    #以文本方式获取请求响应内容
    print(r.text)