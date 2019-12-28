from qiniu import Auth, put_file, etag
from qiniu import BucketManager
import qiniu.config
import requests
import json
import jsonpath
import time
import os
from config import *

access_key = ACCESS_KEY  #AK
secret_key = SECRET_KEY    #SK
bucket_name = BUCKET_NAME   #name
url = QINIU_URL  #url
q = Auth(access_key, secret_key)
from qiniu import Auth,put_data,etag,urlsafe_base64_encode
import logging

#上传大的文件
def qiniu_up_file(keyNmae,localfile):
    try:
        q = Auth(ACCESS_KEY, SECRET_KEY)
        token = q.upload_token(BUCKET_NAME)
        imgname = "{}{}".format(int(time.time()),keyNmae)
        ret,info = put_data(token,imgname,localfile)
    except Exception as e:
        logging.error(e)
        raise Exception("上传文件到七牛云时候出现错误！")
    if info and info.status_code != 200:
        raise Exception("上传文件到七牛云时候出现错误！")
    img_name = ret["key"]
    return QINIUURLNAME+img_name





#up_url_file
def upload_file_url(key, localfile):   # 图片名称
    token = q.upload_token(bucket_name, key, 3600)
    ret, info = qiniu.put_file(token, key, localfile)
    try:
        res = "{0}{1}".format(url, ret['key'])
        return "http://q2cbcbetl.bkt.clouddn.com/" + key
    except:
        return 404