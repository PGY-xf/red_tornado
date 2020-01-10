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



#七牛云删除单个文件

from config import *

access_key = ACCESS_KEY  #AK
secret_key = SECRET_KEY    #SK
bucket_name = BUCKET_NAME   #name
url = QINIU_URL  #url

from qiniu import Auth
from qiniu import BucketManager

def deleteap(picture):
    access_key = ACCESS_KEY
    secret_key = SECRET_KEY
    #初始化Auth状态
    q = Auth(access_key, secret_key)
    #初始化BucketManager
    bucket = BucketManager(q)
    #你要测试的空间， 并且这个key在你空间中存在
    bucket_name = BUCKET_NAME
    key = picture
    #删除bucket_name 中的文件 key
    ret, info = bucket.delete(bucket_name, key)
    print(info)
    # assert ret == {}
