from .base import BaseHandler
from models import *
import json
from components.qiniu_upload import upload_file_url,qiniu_up_file  #第一个直接传url即可 第二个需要传文件
from config import *
from func_tools import *
import random
import time
import datetime
from datetime import timedelta
from func_tools import *
from models import *
import time
import datetime
from datetime import timedelta



#发送手机号验证码
class Phone(BaseHandler):
    def get(self,*args,**kwargs):
        self.render('../templates/phone.html')
    def post(self,*args,**kwargs):
        phone = self.get_argument('phone')
        print(phone)
        isphone = re.match('^1[3,5,7,8]\d{9}$', phone)
        # 数据校验
        if isphone:
            # sample(seq, n) 从序列seq中选择n个随机且独立的元素；
            id = ''.join(str(i) for i in random.sample(range(0, 9), 5))  # 随机数
            # 发送短信
            send_datas(
                to='+86' + phone,
                from_='16788203823',
                body='【验证码】--->:' + id,
            )
            # 存入redis
            redis_conn.set("code", id, ex=120)  # 过期时间 120s
            self.write('短信已发送成功')
            # self.write(json.dumps({"status": 200, "msg": "短信已发送成功"}, ensure_ascii=False, indent=4))
        else:
            self.write('手机号输入不正确')
            # self.write(json.dumps({"status": 1005, "msg": "手机号输入不正确"}, ensure_ascii=False, indent=4))


# class Submits(BaseHandler):
#     def get(self,*args,**kwargs):
#         mes = {}
#         mes['data'] = ''
#         self.render('../templates/phone.html',**mes)
#     def post(self,*args,**kwargs):
#         mes = {}
#         mes['data'] = ''
#         phone = self.get_argument('phone')
#         code = self.get_argument('code')
#         if not all(['phone','code']):
#             mes['data'] = "不能为空"
#             self.render('../templates/phone.html',**mes)
#         else:
#             if code == redis_conn.get("code"):
#                 user = User(phone=phone)
#                 sess.add(user)
#                 sess.commit()
#                 self.render('../templates/phone.html',**mes)
#             else:
#                 mes['data'] = "验证码错误"
#                 self.render('../templates/phone.html',**mes)




# 首页
class Index(BaseHandler):
    @log_decorator
    def get(self, *args, **kwargs):
        self.render('../templates/index.html',)


# 我的桌面
class Welcome(BaseHandler):
    def get(self, *args, **kwargs):
        ip = self.request.remote_ip     #获取的ip
        timess = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())   #当前时间
        system = sess.query(System).filter(System.id==1).one()
                #所有数目
        video = len(sess.query(Video).all())   #电影
        micro_video = len(sess.query(Micro_video).all())  #微视频
        author = len(sess.query(Author).all())   #摄制中心
        user = len(sess.query(User).all())    #用户
        adminUser = len(sess.query(AdminUser).all())  #管理员
            #今天创建的数目
        today = str(datetime.date.today())
        video_now = len(sess.query(Video).filter(Video.create_time.like('%' + today + '%')).all())    #电影
        micro_video_now = len(sess.query(Micro_video).filter(Micro_video.issue_time.like('%' + today + '%')).all())   #微视频
        author_now = len(sess.query(Author).filter(Author.create_time.like('%' + today + '%')).all())    #摄制中心
        user_now = len(sess.query(User).filter(User.create_time.like('%' + today + '%')).all())      ##用户 
        adminUser_now = len(sess.query(AdminUser).filter(AdminUser.create_time.like('%' + today + '%')).all())   #管理员
            #昨天创建的数目
        today = datetime.date.today()
        yesterday = today + datetime.timedelta(days=-1)
        dateyest = str(yesterday.isoformat())
        video_yesterday = len(sess.query(Video).filter(Video.create_time.like('%' + dateyest + '%')).all())    #电影
        micro_video_yesterday = len(sess.query(Micro_video).filter(Micro_video.issue_time.like('%' + dateyest + '%')).all())   #微视频
        author_yesterday = len(sess.query(Author).filter(Author.create_time.like('%' + dateyest + '%')).all())    #摄制中心
        user_yesterday = len(sess.query(User).filter(User.create_time.like('%' + dateyest + '%')).all())      ##用户 
        adminUser_yesterday = len(sess.query(AdminUser).filter(AdminUser.create_time.like('%' + dateyest + '%')).all())   #管理员
            #本周创建的数目 
        now = datetime.datetime.now()
        #本周日期
        today = now
        this1 = (now - datetime.timedelta(days=now.weekday())).strftime('%Y-%m-%d')
        this2 = (now + datetime.timedelta(days=1-now.weekday())).strftime('%Y-%m-%d')
        this3 = (now + datetime.timedelta(days=2-now.weekday())).strftime('%Y-%m-%d')
        this4 = (now + datetime.timedelta(days=3-now.weekday())).strftime('%Y-%m-%d')
        this5 = (now + datetime.timedelta(days=4-now.weekday())).strftime('%Y-%m-%d')
        this6 = (now + datetime.timedelta(days=5-now.weekday())).strftime('%Y-%m-%d')
        this7 = (now + datetime.timedelta(days=6-now.weekday())).strftime('%Y-%m-%d')
            #电影
        video_week1 = len(sess.query(Video).filter(Video.create_time.like('%' + this1 + '%')).all())    #电影
        video_week2 = len(sess.query(Video).filter(Video.create_time.like('%' + this2 + '%')).all())    #电影
        video_week3 = len(sess.query(Video).filter(Video.create_time.like('%' + this3 + '%')).all())    #电影
        video_week4 = len(sess.query(Video).filter(Video.create_time.like('%' + this4 + '%')).all())    #电影
        video_week5 = len(sess.query(Video).filter(Video.create_time.like('%' + this5 + '%')).all())    #电影
        video_week6 = len(sess.query(Video).filter(Video.create_time.like('%' + this6 + '%')).all())    #电影
        video_week7 = len(sess.query(Video).filter(Video.create_time.like('%' + this7 + '%')).all())    #电影
        video_week = video_week1+video_week2+video_week3+video_week4+video_week5+video_week6+video_week7
            #微视频
        micro_video_week1 = len(sess.query(Micro_video).filter(Micro_video.issue_time.like('%' + this1 + '%')).all())   #微视频
        micro_video_week2 = len(sess.query(Micro_video).filter(Micro_video.issue_time.like('%' + this2 + '%')).all())   #微视频
        micro_video_week3 = len(sess.query(Micro_video).filter(Micro_video.issue_time.like('%' + this3 + '%')).all())   #微视频
        micro_video_week4 = len(sess.query(Micro_video).filter(Micro_video.issue_time.like('%' + this4 + '%')).all())   #微视频
        micro_video_week5 = len(sess.query(Micro_video).filter(Micro_video.issue_time.like('%' + this5 + '%')).all())   #微视频
        micro_video_week6 = len(sess.query(Micro_video).filter(Micro_video.issue_time.like('%' + this6 + '%')).all())   #微视频
        micro_video_week7 = len(sess.query(Micro_video).filter(Micro_video.issue_time.like('%' + this7 + '%')).all())   #微视频
        micro_video_week = micro_video_week1+micro_video_week2+micro_video_week3+micro_video_week4+micro_video_week5+micro_video_week6+micro_video_week7
            #摄制中心
        author_week1 = len(sess.query(Author).filter(Author.create_time.like('%' + this1 + '%')).all())    #摄制中心
        author_week2 = len(sess.query(Author).filter(Author.create_time.like('%' + this2 + '%')).all())    #摄制中心
        author_week3 = len(sess.query(Author).filter(Author.create_time.like('%' + this3 + '%')).all())    #摄制中心
        author_week4 = len(sess.query(Author).filter(Author.create_time.like('%' + this4 + '%')).all())    #摄制中心
        author_week5 = len(sess.query(Author).filter(Author.create_time.like('%' + this5 + '%')).all())    #摄制中心
        author_week6 = len(sess.query(Author).filter(Author.create_time.like('%' + this6 + '%')).all())    #摄制中心
        author_week7 = len(sess.query(Author).filter(Author.create_time.like('%' + this7 + '%')).all())    #摄制中心
        author_week = author_week1+author_week2+author_week3+author_week4+author_week5+author_week6+author_week7
            ##用户 
        user_week1 = len(sess.query(User).filter(User.create_time.like('%' + this1 + '%')).all())      ##用户 
        user_week2 = len(sess.query(User).filter(User.create_time.like('%' + this2 + '%')).all())      ##用户 
        user_week3 = len(sess.query(User).filter(User.create_time.like('%' + this3 + '%')).all())      ##用户 
        user_week4 = len(sess.query(User).filter(User.create_time.like('%' + this4 + '%')).all())      ##用户 
        user_week5 = len(sess.query(User).filter(User.create_time.like('%' + this5 + '%')).all())      ##用户 
        user_week6 = len(sess.query(User).filter(User.create_time.like('%' + this6 + '%')).all())      ##用户 
        user_week7 = len(sess.query(User).filter(User.create_time.like('%' + this7 + '%')).all())      ##用户 
        user_week = user_week1+user_week2+user_week3+user_week4+user_week5+user_week6+user_week7
            #管理员
        adminUser_week1 = len(sess.query(AdminUser).filter(AdminUser.create_time.like('%' + this1 + '%')).all())   #管理员
        adminUser_week2 = len(sess.query(AdminUser).filter(AdminUser.create_time.like('%' + this2 + '%')).all())   #管理员
        adminUser_week3 = len(sess.query(AdminUser).filter(AdminUser.create_time.like('%' + this3 + '%')).all())   #管理员
        adminUser_week4 = len(sess.query(AdminUser).filter(AdminUser.create_time.like('%' + this4 + '%')).all())   #管理员
        adminUser_week5 = len(sess.query(AdminUser).filter(AdminUser.create_time.like('%' + this5 + '%')).all())   #管理员
        adminUser_week6 = len(sess.query(AdminUser).filter(AdminUser.create_time.like('%' + this6 + '%')).all())   #管理员
        adminUser_week7 = len(sess.query(AdminUser).filter(AdminUser.create_time.like('%' + this7 + '%')).all())   #管理员
        adminUser_week = adminUser_week1+adminUser_week2+adminUser_week3+adminUser_week4+adminUser_week5+adminUser_week6+adminUser_week7
            #本月创建的数目 
        times = time.strftime("%Y-%m", time.localtime())
        video_month = len(sess.query(Video).filter(Video.create_time.like('%' + times + '%')).all())    #电影
        micro_video_month = len(sess.query(Micro_video).filter(Micro_video.issue_time.like('%' + times + '%')).all())   #微视频
        author_month = len(sess.query(Author).filter(Author.create_time.like('%' + times + '%')).all())    #摄制中心
        user_month = len(sess.query(User).filter(User.create_time.like('%' + times + '%')).all())      ##用户 
        adminUser_month = len(sess.query(AdminUser).filter(AdminUser.create_time.like('%' + times + '%')).all())   #管理员
        self.render('../templates/welcome.html',ip=ip,timess=timess,video=video,micro_video=micro_video,
                    author=author,user=user,adminUser=adminUser,video_now=video_now,micro_video_now=micro_video_now,
                    author_now=author_now,user_now=user_now,adminUser_now=adminUser_now,video_yesterday=video_yesterday,
                    micro_video_yesterday=micro_video_yesterday,author_yesterday=author_yesterday,user_yesterday=user_yesterday,
                    adminUser_yesterday=adminUser_yesterday,video_month=video_month,micro_video_month=micro_video_month,
                    author_month=author_month,user_month=user_month,adminUser_month=adminUser_month,video_week=video_week,
                    micro_video_week=micro_video_week,author_week=author_week,user_week=user_week,adminUser_week=adminUser_week,system=system)




# 评论列表
class Feedment_list(BaseHandler):
    def get(self, *args, **kwargs):
        comment = sess.query(Comment).all()
        lens = len(comment)
        self.render('../templates/feedment_list.html', comment=comment, lens=lens)
    def post(self,*args,**kwargs):
        title = self.get_argument('title', '')
        comment = sess.query(Comment).filter(Comment.name.like('%' + title + '%')).all()
        lens = len(comment)
        pass



# 删除评论
class Feedment_del(BaseHandler):
    def get(self, id):
        comment = sess.query(Comment).filter(Comment.id == id).one()
        sess.delete(comment)
        sess.commit()
        self.redirect('/product_list')


#意见反馈
class Feedback_list(BaseHandler):
    def get(self,*args,**kwargs):
        opinion = sess.query(Opinion).all()
        lens = len(opinion)
        self.render('../templates/feedback_list.html',opinion=opinion,lens=lens)
    def post(self,*args,**kwargs):
        title = self.get_argument('title', '')
        opinion = sess.query(Opinion).filter(Opinion.name.like('%' + title + '%')).all()
        lens = len(opinion)
        pass



# 折线图
class Charts_1(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('../templates/charts_1.html')


# 时间轴折线图
class Charts_2(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('../templates/charts_2.html')


# 区域图
class Charts_3(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('../templates/charts_3.html')


# 柱状图
class Charts_4(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('../templates/charts_4.html')


# 饼状图
class Charts_5(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('../templates/charts_5.html')


# 3D柱状图
class Charts_6(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('../templates/charts_6.html')


# 3D饼状图
class Charts_7(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('../templates/charts_7.html')




# # 系统设置（添加）
# class System_base(BaseHandler):
#     def get(self, *args, **kwargs):
#         self.render('../templates/system_add.html')
#     def post(self, *srgs, **kwsrgs):
#         site_name = self.get_argument('site_name', '')
#         domain_name = self.get_argument('domain_name', '')
#         describe = self.get_argument('describe', '')
#         copyrights = self.get_argument('copyrights', '')
#         number = self.get_argument('number', '')
#         SMTP_server = self.get_argument('SMTP_server', '')
#         SMTP_port = self.get_argument('SMTP_port', '')
#         mail_account = self.get_argument('mail_account', '')
#         email_password = self.get_argument('email_password', '')
#         email_address = self.get_argument('email_address', '')
#         system = System(site_name=site_name,domain_name=domain_name,describe=describe,
#                 number=number,copyrights=copyrights,SMTP_server=SMTP_server,SMTP_port=SMTP_port,
#                 mail_account=mail_account,email_password=email_password,email_address=email_address
#                 )
#         sess.add(system)
#         sess.commit()
#         self.redirect('/system_base')




# 系统设置（修改）
class System_base(BaseHandler):
    def get(self, *args, **kwargs):
        system = sess.query(System).filter_by(id=1).first()
        self.render('../templates/system_base.html',system=system)
    def post(self, *args, **kwargs):
        p = sess.query(System).filter_by(id=1).first()
        site_name = self.get_argument('site_name', '')
        domain_name = self.get_argument('domain_name', '')
        describe = self.get_argument('describe', '')
        copyrights = self.get_argument('copyrights', '')
        number = self.get_argument('number', '')
        SMTP_server = self.get_argument('SMTP_server', '')
        SMTP_port = self.get_argument('SMTP_port', '')
        mail_account = self.get_argument('mail_account', '')
        email_password = self.get_argument('email_password', '')
        email_address = self.get_argument('email_address', '')
        p.site_name = site_name
        p.domain_name = domain_name
        p.describe = describe
        p.copyrights = copyrights
        p.SMTP_server = SMTP_server
        p.SMTP_port = SMTP_port
        p.email_password = email_password
        p.email_address = email_address
        p.number = number
        p.mail_account = mail_account
        sess.commit()
        self.redirect('/system_base')



# 屏蔽词
class System_shielding(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('../templates/system_shielding.html')


class IndexHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.write("Hello, world123")
        # self.finish({'name':'你好'})


###################################################################
import json
import re

class RegisterHanler(BaseHandler):
    async def get(self, *args, **kwargs):
        self.write(json.dumps({"status":200,"msg":"返回成功"},ensure_ascii=False,indent=4))
    async def post(self ,*args ,**kwargs):
        phoneno = self.get_argument('phoneno')
        password = self.get_argument('password')
        code = self.get_argument('code')
        if not all([phoneno,password,code]):
            self.write(json.dumps({'status':10010,'msg':'内容输入不全'},ensure_ascii=False,index=4))
        else:
            if re.match('^1[3578]\d{9}$',phoneno):
                user = sess.query(User).filter(User.phone == phoneno).first()
                if not user:
                    user = User(phone=phoneno,password=password)
                    sess.add(user)
                    sess.commit()
                    self.write(json.dumps({'status':200,'msg':'注册成功'},ensure_ascii=False,indent=4))
                else:
                    self.write(json.dumps({'status':10011,'msg':'手机号已注册'},ensure_ascii=False,indent=4))
            else:
                self.write(json.dumps({'status':10012,'msg':'手机号格式不正确'},ensure_ascii=False,indent=4))




class LoginHanler(BaseHandler):
    async def get(self, *args, **kwargs):
        self.write(json.dumps({'status':200,'msg':'返回成功'},ensure_ascii=False,indent=4))
    async def post(self, *args, **kwargs):
        phoneno = self.get_argument('phoneno')
        password = self.get_argument('password')
        if not all([phoneno,password]):
            self.write(json.dumps({'status':10010,'msg':'内容输入不全'},ensure_ascii=False,indent=4))
        else:
            user = sess.query(User).filter(User.phone==phoneno).first()
            if user:
                if user.password == password:
                    self.write(json.dumps({'status':200,'msg':'登录成功'},ensure_ascii=False,indent=4))
                else:
                    self.write(json.dumps({'status':10010,'msg':'密码错误，请重新输入'},ensure_ascii=False,indent=4))
            else:
                self.write(json.dumps({'status':10011,'msg':'用户名不存在，请注册'},ensure_ascii=False,indent=4))

            

     

class IndexHanler(BaseHandler):
    async def get(self, *args, **kwargs):
        self.write(json.dumps({'status':200,'msg':'返回成功'},ensure_ascii=False,indent=4))
    async def post(self, *args, **kwargs):
        pass


