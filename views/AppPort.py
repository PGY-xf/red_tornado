import random

from .base import BaseHandler
from models import *
import json
from components import qiniu_upload
from qiniu import Auth, put_file, etag
from qiniu import BucketManager
import qiniu.config
import requests
import json
import jsonpath
import time
import os
from config import *
from qiniu import Auth,put_data,etag,urlsafe_base64_encode
import logging

access_key = ACCESS_KEY  #AK
secret_key = SECRET_KEY    #SK
bucket_name = BUCKET_NAME   #name
url = QINIU_URL  #url

class GetToken(BaseHandler):
    def get(self, *args, **kwargs):
        # 需要填写你的 Access Key 和 Secret Key
        access_key = ACCESS_KEY
        secret_key = SECRET_KEY
        # 构建鉴权对象
        q = Auth(access_key, secret_key)
        # 要上传的空间
        bucket_name = BUCKET_NAME
        # 上传后保存的文件名
        key = 'token'
        # 生成上传 Token，可以指定过期时间等
        # 上传策略示例
        # https://developer.qiniu.com/kodo/manual/1206/put-policy
        domain = "http://q2cbcbetl.bkt.clouddn.com/"
        policy = {
            'callbackUrl': 'https://requestb.in/1c7q2d31',
            'callbackBody': 'filename=$(fname)&filesize=$(fsize)',
            'persistentOps': 'imageView2/1/w/200/h/200'
        }
        # 3600为token过期时间，秒为单位。3600等于一小时
        token = q.upload_token(bucket_name, key, 3600, policy)
        print("有人取走了token")
        self.write(json.dumps({"uptoken":token,"domain":domain }, ensure_ascii=False))

#七牛云token
class QiNiuHandler(BaseHandler):
    async def get(self):
        q = Auth('E2IZM3koC1GR1DUqJHactmixzdyZZhx0edBKqDsk','GDnMkvRoE_kFhCSuvdqQj0VcNsRDOHzYJJ_bVd0_')
        token = q.upload_token('redinnovation')
        print("有人过来取走了token")
        self.write(json.dumps({'uptoken':token},ensure_ascii=False))



# 后台首页
# 首页
class Ceshi(BaseHandler):
    def get(self, *args, **kwargs):
        print("有人对我发起了请求！")
        goods_list = "请求到了页面！"
        return self.write(json.dumps({"status": 200, "msg": "返回成功", 'goods': goods_list}, cls=AlchemyEncoder, ensure_ascii=False))


#推荐页微视频
class gitVideolist(BaseHandler):
    def get(self, id,*args, **kwargs):
        id = int(id)
        # microall =random.sample(sess.query(Micro_video).filter(Micro_video.video_url!=None).all(),10)
        microall = sess.query(Micro_video).filter(Micro_video.video_url!=None).all()[id:id+10]
        video_list = []
        for micro in microall:
            item = {}
            item["id"] = micro.id
            item["title"] = micro.name

            item["playnum"] = micro.amount
            try:
                item["video_img"] = micro.video_img
            except:
                item["video_img"]=""
            try:
                item["video_url"] = micro.video_url
            except:
                item["video_url"] = ""
            try:
                item["length"] = micro.length
            except:
                item["length"] = ""
            author = sess.query(Author.id,Author.name, Author.img).filter(Author.id == micro.auth_id)
            item["column_id"] = author[0][0]
            item["column_name"] = author[0][1]
            item["column_img"] = author[0][2]
            video_list.append(item)
        return self.write(json.dumps({"status": 200, "msg": "返回成功", 'video_list':video_list}, cls=AlchemyEncoder, ensure_ascii=False))


 
#主页栏目的四个视频
class gitColumnsVideofourList(BaseHandler):
    def get(self, *args, **kwargs):
        listitem = []
        columns = sess.query(Columns).all()
        for col in columns:
            item = {}
            item["colums_id"] = col.id
            item["headerTitle"] = col.name
            item["bodyList"] = []
            microall = sess.query(Micro_video).filter(Micro_video.video_url != None, Micro_video.is_show == 1,
                                                      Micro_video.column_id == col.id).all()[:4]
            for vid in microall:
                videoobj = {}
                videoobj["id"] = vid.id
                videoobj["title"] = vid.name
                videoobj["info"] = vid.info
                videoobj["img"] = vid.video_img
                videoobj["video_url"] = vid.video_url
                videoobj["lookNum"] = vid.amount
                videoobj["isHot"] = "true"
                item["bodyList"].append(videoobj)
            listitem.append(item)
        return self.write(json.dumps({"status": 200, "msg": "返回成功", 'columnsVideoList':listitem}, cls=AlchemyEncoder, ensure_ascii=False))