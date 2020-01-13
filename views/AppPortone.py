import random
import string
import re
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
from func_tools import *
from werkzeug.security import generate_password_hash,check_password_hash



# app发送短信验证
class Send_Data(BaseHandler):
    def get(self, *args, **kwargs):
        self.write(json.dumps({"status": 200, "msg": "返回成功"}, ensure_ascii=False, indent=4))
    async def post(self, *args, **kwargs):
        # 接收数据
        phone = self.get_argument('phone')
        isphone = re.match('^1[3,5,7,8]\d{9}$', phone)
        # 数据校验
        if isphone:
            # sample(seq, n) 从序列seq中选择n个随机且独立的元素；
            id = ''.join(str(i) for i in random.sample(range(0, 9), 5))  # 随机数
            # 发送短信
            send_data(
                to= str(phone),
                body=id,
            )
            # 存入redis
            redis_conn.set("code", id, ex=120)  # 过期时间 120s
            self.write(json.dumps({"status": 200, "msg": "短信已发送成功"}, ensure_ascii=False, indent=4))
        else:
            self.write(json.dumps({"status": 1005, "msg": "手机号输入不正确"}, ensure_ascii=False, indent=4))


# APP账号注册
class App_register(BaseHandler):
    def post(self, *args, **kwargs):
        phone = self.get_argument("phoneno")
        password = self.get_argument("password")
        code = self.get_argument("code")
        invitation = self.get_argument("invitation")
        #不需要做对手机号重复的判断，只需要对验证码进行判断。
        #拿到验证码之后去缓存库中判断，以key：手机号  val:验证码
        if not all([phone,password,code]):
            self.write(json.dumps({"status": 1005, "msg": "参数不能为空"}, ensure_ascii=False, indent=4))
        else:
            user = sess.query(User).filter(User.phone == phone).first()
            if not user:   
                if re.match('^1[3,5,7,8]\d{9}$', phone):
                    if int(code) == int(redis_conn.get("code")):
                        users = User(password=generate_password_hash(password), phone=phone)
                        # 添加实例化对象
                        sess.add(users)
                        # 提交保存数据
                        sess.commit()
                        self.write(json.dumps({"status": 200, "msg": "注册成功"}, ensure_ascii=False, indent=4))
                    else:
                        self.write(json.dumps({"status": 10010, "msg": "验证码错误"}, ensure_ascii=False, indent=4))
                else:
                    self.write(json.dumps({"status": 10012, "msg": "手机号格式不正确"}, ensure_ascii=False, indent=4))
            else:
                self.write(json.dumps({"status": 10011, "msg": "用户已注册"}, ensure_ascii=False, indent=4))




#app登录
class App_login(BaseHandler):
    def post(self, *args, **kwargs):
        phone = self.get_argument("phoneno")
        password = self.get_argument("password")
        print(phone)
        print(password)
        if not all(phone,password):
            return self.write(json.dumps({"status": 10010, "msg": "参数不能为空！"}, cls=AlchemyEncoder,ensure_ascii=False))
        else:
            try:
                user_info = sess.query(User).filter(User.phone==phone,password==password).one()
                if check_password_hash(user_info.password,password):
                    return self.write(json.dumps({"status": 200, "msg": "登录成功！", "user_info": user_id}, cls=AlchemyEncoder,ensure_ascii=False))
                else:
                    return self.write(json.dumps({"status": 10011, "msg": "密码错误"}, cls=AlchemyEncoder,ensure_ascii=False))
            except:
                return self.write(json.dumps({"status": 10012, "msg": "用户不存在"}, cls=AlchemyEncoder,ensure_ascii=False))




# 微视频视频详情页
class gitVideodetails(BaseHandler):
    def get(self, *args, **kwargs):
        # id = int(id) 
        id = 1
        micro_video = sess.query(Micro_video).filter(Micro_video.id==id).one()
        author = sess.query(Author).filter(Author.id==micro_video.auth_id).one()
        item = {}
        item['id'] = micro_video.id
        item['video_url'] = micro_video.video_url
        item['name'] = author.name
        return self.write(json.dumps({"status": 200, "msg": "返回成功", "filmvideolist": item}, cls=AlchemyEncoder,ensure_ascii=False))


#栏目列表
class gitColumnsList(BaseHandler):
    def get(self, *args, **kwargs):
        columns = sess.query(Columns).all()
        column_list = []
        for info in columns:
            item = {}
            item["id"] = info.id
            item["name"] = info.name
            item["columns_img"] = info.columns_img
            column_list.append(item)
        return self.write(json.dumps({"status": 200, "msg": "返回成功","column_list":column_list[:10]}, cls=AlchemyEncoder,ensure_ascii=False))
  

#标签列表
class gitlabelList(BaseHandler):
    def get(self, *args, **kwargs):
        label = sess.query(Label).all()
        label_list = []
        for info in label:
            item = {}
            item["id"] = info.id
            item["name"] = info.name
            item["label_img"] = info.label_img
            label_list.append(item)
        return self.write(json.dumps({"status": 200, "msg": "返回成功","label_list":label_list[:10]}, cls=AlchemyEncoder,ensure_ascii=False))


#公告列表
class getnotice(BaseHandler):
    def get(self, *args, **kwargs):
        notice = sess.query(Notice).all()
        notice_list = []
        for info in notice:
            item = {}
            item["id"] = info.id
            item["name"] = info.name
            item["notice_img"] = info.notice_img
            item["notice_link"] = info.notice_link
            item["is_show"] = info.is_show
            notice_list.append(item)
        return self.write(json.dumps({"status": 200, "msg": "返回成功","notice_list":notice_list[:10]}, cls=AlchemyEncoder,ensure_ascii=False))



#广告列表
class getadvertising(BaseHandler):
    def get(self, *args, **kwargs):
        advertising = sess.query(Advertising).all()
        advertising_list = []
        for info in advertising:
            item = {}
            item["id"] = info.id
            item["name"] = info.name
            item["advertising_img"] = info.advertising_img
            item["advertising_link"] = info.advertising_link
            item["is_show"] = info.is_show
            advertising_list.append(item)
        return self.write(json.dumps({"status": 200, "msg": "返回成功","advertising_list":advertising_list[:10]}, cls=AlchemyEncoder,ensure_ascii=False))



