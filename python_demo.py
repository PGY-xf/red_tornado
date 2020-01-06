from urllib import request
from urllib import parse

import urllib.request
import time
import hashlib
import random

print ("python demo starting...")

url = "https://openapi.miaodiyun.com/distributor/sendSMS"
accountSid="2b9e685e60c32a0cff712b723f2fabb5"
to="15603817663"
templateid="244343"
param= ''.join(str(i) for i in random.sample(range(0, 9), 6))
auth_token="a39ccc400352aa17bc980f5f2a71cd15"

t = time.time()
timestamp = str((int(round(t * 1000))))
sig=accountSid+auth_token+timestamp
m1 = hashlib.md5()
m1.update(sig.encode("utf-8"))
sig = m1.hexdigest()	

data="accountSid="+accountSid+"&to="+to+"&templateid="+templateid+"&param="+param+"&timestamp="+timestamp+"&sig="+sig
headers = {   
    'Content-Type':'application/x-www-form-urlencoded',
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36'
}
data=str.encode(data)

print("data sent to SMS server is:")
print(data)
req = request.Request(url, headers=headers, data=data)  #POST方法
page = request.urlopen(req).read()
page = page.decode('utf-8')
print("response from SMS server is:")
print(page)

print ("python demo finished")







# #  编码说明：coding=utf-8或gbk
# from CCPRestSDK import REST
# import ConfigParser
 
# accountSid= '8a216da86f696570016f6ac8b4cf0175'
#  #说明：主账号，登陆云通讯网站后，可在控制台首页中看到开发者主账号ACCOUNT SID。
 
# accountToken= '2375869565ee41659a3b079dc6eb7b44'
#  #说明：主账号Token，登陆云通讯网站后，可在控制台首页中看到开发者主账号AUTH TOKEN。
 
# appId='8a216da86f696570016f6ac8b52c017b' 
#  #请使用管理控制台中已创建应用的APPID。
 
# serverIP='app.cloopen.com'
#  #说明：请求地址，生产环境配置成app.cloopen.com。
 
# serverPort='8883' 
#  #说明：请求端口 ，生产环境为8883.
 
# softVersion='2013-12-26' #说明：REST API版本号保持不变。 
 
# def sendTemplateSMS(to,datas,tempId): 
#     #初始化REST SDK
#     rest = REST(serverIP,serverPort,softVersion) 
#     rest.setAccount(accountSid,accountToken) 
#     rest.setAppId(appId)
 
#     result = rest.sendTemplateSMS(to,datas,tempId) 
#     for k,v in result.iteritems():
#         if k=='templateSMS' : 
#             for k,s in v.iteritems():
#                 print('%s:%s' % (k, s))
#         else: 
#             print( '%s:%s' % (k, v) )
 
# #  可参考demo中的接口调用文件：SendTemplateSMS.py。
