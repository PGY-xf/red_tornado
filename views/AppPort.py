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





# 生成四位随机数字
def getCode():
    seeds = string.digits
    random_str = random.choices(seeds, k=4)
    number = "".join(random_str)
    return number


# APP获取验证码
class App_getverification(BaseHandler):
    def post(self, *args, **kwargs):
        code_type = self.get_argument("code_type")
        # 先判断是那边调取的验证码，然后再去做事情。
        if code_type == "reg":
            phone = self.get_argument("phoneno")
            # 判断用户是否输入了手机号
            isphone = re.match('^1[3,5,7,8]\d{9}$', phone)
            if isphone:
                # 判断次手机号是否已经注册
                user = sess.query(User).filter(User.phone == phone).first()
                # 如果user不存在则进行注册：
                if not user:
                    # 生成验证并将验证码发送到用户手机号上！
                    phone = phone
                    codeNum = getCode()
                    return self.write(
                        json.dumps({"status": 200, "msg": "验证码:" + codeNum}, cls=AlchemyEncoder,
                                   ensure_ascii=False))
                # 如果存在则提醒已注册
                else:
                    return self.write(
                        json.dumps({"status": 200, "msg": "手机号已注册！"}, cls=AlchemyEncoder,
                                   ensure_ascii=False))
            # 手机号格式错误
            else:
                return self.write(
                    json.dumps({"status": 201, "msg": "手机号格式错误。"}, cls=AlchemyEncoder, ensure_ascii=False))
        else:
            return self.write(
                json.dumps({"status": 201, "msg": "请添加验证码类型！"}, cls=AlchemyEncoder, ensure_ascii=False))


# APP账号注册
class App_register_user(BaseHandler):
    def post(self, *args, **kwargs):
        phone = self.get_argument("phoneno")
        print("手机号为{}的用户申请注册".format(phone))
        password = self.get_argument("password")
        code = self.get_argument("code")
        invitation = self.get_argument("invitation")
        #不需要做对手机号重复的判断，只需要对验证码进行判断。
        #拿到验证码之后去缓存库中判断，以key：手机号  val:验证码
        if code:
            add_user = User(phone=phone,password=generate_password_hash(password),name=phone,user_img="/static/common/default_userimg.jpg")
            sess.add(add_user)
            sess.commit()
            return self.write(
                json.dumps({"status": 200, "msg": "注册成功快去登录把！"}, cls=AlchemyEncoder,
                           ensure_ascii=False))
        else:
            return self.write(
                json.dumps({"status": 200, "msg": "验证码错误！"}, cls=AlchemyEncoder,
                           ensure_ascii=False))


# APP账号登录
class App_login_user(BaseHandler):
    def post(self, *args, **kwargs):
        phone = self.get_argument("phoneno")
        password = self.get_argument("password")
        user_info = sess.query(User).filter(User.phone==phone,password==password).one()
        if user_info:
            item = {}
            item["userid"] = user_info.id
            return self.write(
                json.dumps({"status": 200, "msg": "登录成功！", "user_info": item}, cls=AlchemyEncoder,
                           ensure_ascii=False))
        else:
            return self.write(
                json.dumps({"status": 201, "msg": "登录失败"}, cls=AlchemyEncoder,
                           ensure_ascii=False))




#获取登录用户的信息
class Get_APP_loginuserinfo(BaseHandler):
    def post(self, *args, **kwargs):
        userid = self.get_argument("userId")
        userinfo = sess.query(User).filter(User.id == userid).one()
        # 判断是否有该用户如果有则返回信息
        if userinfo:
            item = {}
            item["userId"] = userinfo.id
            item["userName"] = userinfo.name
            item["userImg"] = userinfo.user_img
            item["userHistoryList"] = []
            return self.write(
                json.dumps({"status": 200, "msg": "登录成功！", "user_info": item}, cls=AlchemyEncoder,
                           ensure_ascii=False))
        else:
            return self.write(
                json.dumps({"status": 201, "msg": "没有此用户！"}, cls=AlchemyEncoder,
                           ensure_ascii=False))


#用户修改密码
class APP_user_update_password(BaseHandler):
    def post(self, *args, **kwargs):
        userid = self.get_argument("userid")
        oldpassword = self.get_argument("oldpassword")
        newpassword= self.get_argument("newpassword")
        useruppassword = sess.query(User).filter(User.id==userid).one()
        if useruppassword:
            if useruppassword.password==oldpassword:
                useruppassword.password = newpassword
                sess.commit()
                return self.write(
                    json.dumps({"status": 200, "msg": "密码修改成功！"}, cls=AlchemyEncoder,
                               ensure_ascii=False))
            else:
                return self.write(
                    json.dumps({"status": 200, "msg":"旧密码输入错误！"}, cls=AlchemyEncoder,
                               ensure_ascii=False))
        else:
            return self.write(
                json.dumps({"status": 201, "msg": "出了点问题请稍后重试！"}, cls=AlchemyEncoder,
                           ensure_ascii=False))




# 获取主持人列表
class getIndexCompere_list(BaseHandler):
    def get(self, *args, **kwargs):
        mingxing_info = sess.query(Big_V).all()
        pro_list = []
        for info in mingxing_info:
            item = {}
            item["id"] = info.id
            item["name"] = info.name
            item["english_name"] = info.english_name
            item["year"] = info.year
            item["gender"] = info.gender
            item["nation"] = info.nation
            item["nationality"] = info.nationality
            item["big_v_img1"] = info.big_v_img1
            item["big_v_img2"] = info.big_v_img2
            item["director"] = info.director
            item["profession"] = info.profession
            item["region"] = info.region
            item["graduate_academy"] = info.graduate_academy
            item["blood_type"] = info.blood_type
            item["stature"] = info.stature
            item["blood_type"] = info.blood_type
            item["weight"] = info.weight
            item["constellation"] = info.constellation
            item["main_achievements"] = info.main_achievements.split('、')
            item["in_work"] = info.in_work.split('、')

            item["profession"] = info.profession.split('、')
            for pro in item["profession"]:
                if pro == "主持人":
                    pro_list.append(item)
                else:
                    pass
        return self.write(
            json.dumps({"status": 200, "msg": "返回成功","zhuchiren_list":pro_list[:10]}, cls=AlchemyEncoder,
                       ensure_ascii=False))


#明星详情页
class getIndexCompere_particulars(BaseHandler):
    def get(self,id, *args, **kwargs):
        id = int(id)
        mingxing_info = sess.query(Big_V).filter(Big_V.id==id).one()
        item = {}
        item["id"] = mingxing_info.id
        item["name"] = mingxing_info.name
        item["english_name"] = mingxing_info.english_name
        item["year"] = mingxing_info.year
        item["gender"] = mingxing_info.gender
        item["nation"] = mingxing_info.nation
        item["nationality"] = mingxing_info.nationality
        item["big_v_img1"] = mingxing_info.big_v_img1
        item["big_v_img2"] = mingxing_info.big_v_img2
        item["director"] = mingxing_info.director
        item["profession"] = mingxing_info.profession
        item["region"] = mingxing_info.region
        item["graduate_academy"] = mingxing_info.graduate_academy
        item["blood_type"] = mingxing_info.blood_type
        item["stature"] = mingxing_info.stature
        item["blood_type"] = mingxing_info.blood_type
        item["weight"] = mingxing_info.weight
        item["constellation"] = mingxing_info.constellation
        item["main_achievements"] = mingxing_info.main_achievements.split('、')
        item["in_work"] = mingxing_info.in_work.split('、')
        item["profession"] = mingxing_info.profession.split('、')
        return self.write(
            json.dumps({"status": 200, "msg": "返回成功", "zhuchiren_info": item}, cls=AlchemyEncoder,
                       ensure_ascii=False))



#主页-电影-视频列表
class getIndexfilm_videolist(BaseHandler):
    def get(self, *args, **kwargs):
        # id 名字  视频图片  播放次数  热度
        videoinfoList = []
        videoObj = sess.query(Video.id,Video.name,Video.video_img1,Video.amount,Video.hot,Video.intro).filter(
            Video.video_src != None, Video.is_show == 1,Video.video_img1 != None).all()
        for videoinfo in videoObj:
            item = {}
            item["id"] = videoinfo[0]
            item["title"] = videoinfo[1]
            item["img"] = videoinfo[2]
            item["lookNum"] = videoinfo[3]+3000
            if videoinfo[4] > 5:
                item["isHot"] = True
            else:
                item["isHot"] = False
            item["info"] = videoinfo[5][:13] + "..."
            videoinfoList.append(item)
            # print(item)
        return self.write(
            json.dumps({"status": 200, "msg": "返回成功", "filmvideolist": videoinfoList[:4]}, cls=AlchemyEncoder,
                       ensure_ascii=False))

