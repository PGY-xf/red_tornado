#导包 导入客户端
'''美国号发送邮件'''
from twilio.rest import Client
def send_datas(to,from_,body):
    #定义短信sid
    account_sid = 'AC929f1e9c0bd7f0f2881c731ab816c238'
    #定义秘钥
    auth_token = 'ce02c6f53eaf2154d654d3ec3c224b66'
    #定义客户端对象 
    client = Client(account_sid,auth_token)

    message = client.messages.create(
    to=to,     # 接受短信的手机号，也就是注册界面验证过的那个自己的手机号，注意 写中国区号  +86
    from_=from_,   # 发送短信的美国手机号  区号 +1
    body=body)

    print(message)

from urllib import request
from urllib import parse

import urllib.request
import time
import hashlib
import random

def send_data(to,body):
    url = "https://openapi.miaodiyun.com/distributor/sendSMS"
    accountSid="2b9e685e60c32a0cff712b723f2fabb5"
    templateid="244519"
    auth_token="a39ccc400352aa17bc980f5f2a71cd15"
    t = time.time()
    timestamp = str((int(round(t * 1000))))
    sig=accountSid+auth_token+timestamp
    m1 = hashlib.md5()
    m1.update(sig.encode("utf-8"))
    sig = m1.hexdigest()	

    data="accountSid="+accountSid+"&to="+to+"&templateid="+templateid+"&param="+body+"&timestamp="+timestamp+"&sig="+sig
    headers = {   
        'Content-Type':'application/x-www-form-urlencoded',
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36'
    }
    data=str.encode(data)

    req = request.Request(url, headers=headers, data=data)  #POST方法
    page = request.urlopen(req).read()
    page = page.decode('utf-8')


# id = ''.join(str(i) for i in random.sample(range(0, 9), 5))  # 随机数
# send_data(str(15030090795),id)

'''redis连接'''
import redis
redis_conn = redis.Redis(host="localhost", port=6379)



