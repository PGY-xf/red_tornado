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


# import tornado.web
# import tornado.gen

#app登录
class App_login(BaseHandler):
    # @tornado.web.asynchronous  
    # @tornado.gen.coroutine     #异步
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



# # Comment评论表   Video电影表
# #评论
# class Aaaa(BaseHandler):
#     def get(self,*args,**kwargs):
#         mes = {}
#         mes['data'] = ''
#         video = sess.query(Video).filter_by(id=1).first()
#         comment = sess.query(Comment).filter(Comment.video_id==1).all()
#         self.render('../templates/aaaa.html',video=video,comment=comment,**mes)
#     def post(self,*args,**kwargs):
#         mes = {}
#         mes['data'] = ''
#         video = sess.query(Video).filter_by(id=1).first()
#         comment = sess.query(Comment).filter(Comment.video_id==1).all()
#         count = self.get_argument('count')
#         if not count:
#             mes['data'] = "参数不能为空"
#             self.render('../templates/aaaa.html',video=video,comment=comment,**mes)
#         else:
#             content = Comment(
#                     content=count,
#                     user_id=1,
#                     video_id=1
#                     )
#             sess.add(content)
#             sess.commit()
#             self.redirect('/aaaa')



# class Aaaapp(BaseHandler):
#     def get(self,*args,**kwargs):
#         self.render('../templates/aaaapp.html')




 
# from pay import AliPay

# #初始化阿里支付对象
# def get_ali_object():
#     # 沙箱环境地址：https://openhome.alipay.com/platform/appDaily.htm?tab=info
#     app_id = "2016100100641427"  #  APPID （沙箱应用）

#     # 支付完成后，支付偷偷向这里地址发送一个post请求，识别公网IP,如果是 192.168.20.13局域网IP ,支付宝找不到，def page2() 接收不到这个请求
#     notify_url = "/alipayreturn"

#     # 支付完成后，跳转的地址。
#     return_url = "/alipayreturn"

#     #秘钥地址
#     key_path = os.path.dirname(os.path.dirname(__file__))+"/keys/"
    
#     merchant_private_key_path = key_path+"app_private_2048.txt" # 应用私钥
#     alipay_public_key_path = key_path+"alipay_public_2048.txt"  # 支付宝公钥
#     alipay = AliPay(
#         appid=app_id,
#         app_notify_url=notify_url,
#         return_url=return_url,
#         app_private_key_path=merchant_private_key_path,
#         alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
#         debug=True,  # 默认False,
#     )
#     return alipay





# import random
# #支付宝支付
# class PayPageHandler(BaseHandler):
#     async def post(self):
#         abc = random.randint(0000000,9999999)
#         # 根据当前用户的配置，生成URL，并跳转。
#         money = self.get_argument('money')
#         print(money)
#         a = float(money)
#         b = round(a,2)
#         alipay = get_ali_object()

#         # 生成支付的url
#         query_params = alipay.direct_pay(
#             subject="央视融媒",  # 商品简单描述
#             out_trade_no= str(get_order_code()) + str(abc),  # 用户购买的商品订单号（每次不一样） 20180301073422891
#             total_amount=b,  # 交易金额(单位: 元 保留俩位小数)
#         )

#         pay_url = "https://openapi.alipaydev.com/gateway.do?{0}".format(query_params)  # 支付宝网关地址（沙箱应用）
#         self.write(pay_url)




 
# #支付宝回调
# class PayRetrunHandler(BaseHandler):
#     def get(self):
#         params = self.request.arguments
#         print(params)
#         order = Order(
#             id = str(params['trade_no'][0],'utf-8'),
#             order_amout = str(params['total_amount'][0],'utf-8'),
#             payment_generation_time = str(params['timestamp'][0],'utf-8'),
#             outer_traed_number = str(params['out_trade_no'][0],'utf-8')
#             )
#         sess.add(order)
#         sess.commit()
#         self.redirect('checkout')



# #支付宝退款
# class Refund(BaseHandler):
#     def post(self):
#         money = self.get_argument('money','')  #商品总价
#         id = self.get_argument('id','')        #商品订单号
#         #实例化支付类
#         alipay = get_ali_object()
#         #调用退款方法
#         order_string = alipay.api_alipay_trade_refund(
#             out_trade_no = id,                               #订单号，一定要注意，这是支付成功后返回的唯一订单号
#             refund_amount= money,                            #退款金额，注意精确到分，不要超过订单支付总金额
#             notify_url='/alipayreturn'  #回调网址
#         )
#         order = sess.query(Order).filter(Order.outer_traed_number==id).one()
#         order.trading_status = 2
#         sess.commit()
#         self.write(json.dumps({"status":200,"msg":"退款成功,请注意查看"},ensure_ascii=False,indent=4))