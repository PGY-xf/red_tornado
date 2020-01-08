from .base import BaseHandler
from models import *
import json
from components.qiniu_upload import upload_file_url,qiniu_up_file  #第一个直接传url即可 第二个需要传文件
import os
import qiniu.config
import logging
from config import *
from qiniu import Auth,put_data,etag,urlsafe_base64_encode
import time
from werkzeug.security import generate_password_hash,check_password_hash


# 登录
class Login(BaseHandler):
    def get(self, *args, **kwargs):
        mes = {}
        mes['data'] = ''
        self.render('../templates/login.html',**mes)
    def post(self, *args, **kwargs):
        mes = {}
        mes['data'] = ''
        account = self.get_argument("account","")
        password = self.get_argument("password","")
        print(account,password)
        if not all([account,password]):
            mes['data'] = "不能为空"
            self.render('../templates/login.html',**mes)
        else:
            try:
                adminuser = sess.query(AdminUser).filter(AdminUser.account==account).one()
                if check_password_hash(adminuser.password,password):
                    self.set_cookie('cookie',adminuser.account)
                    self.set_cookie('id',str(adminuser.id))
                    self.redirect('/')
                else:
                    mes['data'] = "密码错误"
                    self.render('../templates/login.html',**mes)
            except:
                mes['data'] = "管理员不存在"
                self.render('../templates/login.html',**mes)


#注册
class Register(BaseHandler):
    def get(self, *args, **kwargs):
        mes = {}
        mes['data'] = ''
        self.render('../templates/register.html',**mes)
    def post(self, *args, **kwargs):
        mes = {}
        mes['data'] = ''
        account = self.get_argument("account","")
        password1 = self.get_argument("password1","")
        password2 = self.get_argument("password2","")
        print(account,password1,password2)
        if not all([account,password1,password2]):
            mes['data'] = "不能为空"
            self.render('../templates/register.html',**mes)
        else:
            if password1 == password2:
                adminuser = sess.query(AdminUser).filter(AdminUser.account==account).first()
                if not adminuser:
                    adminuser = AdminUser(account=account,password=generate_password_hash(password1))
                    sess.add(adminuser)
                    sess.commit()
                    self.redirect('/login')
                else:
                    mes['data'] = "管理员已存在,可添加其他"
                    self.render('../templates/register.html',**mes)
            else:
                mes['data'] = "两次密码输入不符，请重新注册"
                self.render('../templates/register.html',**mes)
                

#摄制组登录
class Login_camera(BaseHandler):
    def get(self, *args, **kwargs):
        mes = {}
        mes['data'] = ''
        self.render('../templates/camera/login_camera.html',**mes)
    def post(self, *args, **kwargs):
        mes = {}
        mes['data'] = ''
        account = self.get_argument("account","")
        password = self.get_argument("password","")
        print(account,password)
        if not all([account,password]):
            mes['data'] = "不能为空"
            self.render('../templates/camera/login_camera.html',**mes)
        else:
            try:
                author = sess.query(Author).filter(Author.account==account).one()
                if check_password_hash(author.password,password):
                    self.set_cookie('cookie',author.account)
                    self.set_cookie('id',str(author.id))
                    self.redirect('/lindex')
                else:
                    mes['data'] = "密码错误"
                    self.render('../templates/camera/login_camera.html',**mes)

            except:
                mes['data'] = "摄制中心不存在"
                self.render('../templates/camera/login_camera.html',**mes)



#摄制组首页
class Lindex(BaseHandler):
    @log_camera
    def get(self, *args, **kwargs):
        self.render('../templates/camera/lindex.html')




#微视频管理
class Lmicro(BaseHandler):
    def get(self, *args, **kwargs):
        cookie = self.get_cookie('cookie')
        suthor = sess.query(Author).filter(Author.account==cookie).one()
        micro_video = sess.query(Micro_video).filter(Micro_video.auth_id==suthor.id).all()
        lens = len(micro_video)
        m_list = []
        for video in micro_video:
            item={}
            item["id"] = video.id
            item["name"]=video.name
            #图片
            item["video_img"] = video.video_img
            #链接
            item["video_url"] = video.video_url
            item["video_slideshow"] = video.video_slideshow
            item["is_show"] = video.is_show
            item["show_time"] = video.issue_time
            try:
                auth = sess.query(Author.name,Author.id).filter(Author.id==video.auth_id)
                item["auth_name"] = auth[0][0]
                item["auth_id"] = auth[0][1]
            except:
                item["auth_name"] = ""
                item["auth_id"] = ""
            try:
                columns = sess.query(Columns.id,Columns.name).filter(Columns.id==video.column_id)
                item["column_id"]=columns[0][0]
                item["column_name"] = columns[0][1]
            except:
                item["column_id"] = ""
                item["column_name"] = ""
            m_list.append(item)
            # print(m_list[0])
        self.render('../templates/camera/lmicro.html', micro_video=m_list, lens=lens)
    def post(self,*args,**kwargs):
        title = self.get_argument('title', '')
        cookie = self.get_cookie('cookie')
        suthor = sess.query(Author).filter(Author.account==cookie).one()
        micro_video = sess.query(Micro_video).filter(Micro_video.auth_id==suthor.id,Micro_video.name.like('%' + title + '%')).all()
        lens = len(micro_video)
        m_list = []
        for video in micro_video:
            item={}
            item["id"] = video.id
            item["name"]=video.name
            #图片
            item["video_img"] = video.video_img
            #链接
            item["video_url"] = video.video_url
            item["video_slideshow"] = video.video_slideshow
            item["is_show"] = video.is_show
            item["show_time"] = video.issue_time
            try:
                auth = sess.query(Author.name,Author.id).filter(Author.id==video.auth_id)
                item["auth_name"] = auth[0][0]
                item["auth_id"] = auth[0][1]
            except:
                item["auth_name"] = ""
                item["auth_id"] = ""
            try:
                columns = sess.query(Columns.id,Columns.name).filter(Columns.id==video.column_id)
                item["column_id"]=columns[0][0]
                item["column_name"] = columns[0][1]
            except:
                item["column_id"] = ""
                item["column_name"] = ""
            m_list.append(item)
        self.render('../templates/camera/lmicro.html', micro_video=m_list, lens=lens)



#添加微视频
class Lmicro_add(BaseHandler):
    def get(self, *args, **kwargs):
        cookie = self.get_cookie('cookie')
        mes = {}
        mes['data'] = ''
        author = sess.query(Author).filter(Author.account==cookie).one()
        columns = sess.query(Columns).filter(Columns.name=='摄制中心小视频').one()
        self.render('../templates/camera/lmicro_add.html',author=author,columns=columns,**mes)
    def post(self, *args, **kwargs):
        cookie = self.get_cookie('cookie')
        author = sess.query(Author).filter(Author.account==cookie).one()
        columns = sess.query(Columns).filter(Columns.name=='摄制中心小视频').one()
        mes = {}
        mes['data'] = ''
        name = self.get_argument('name','')
        info = self.get_argument('info','')
        video_img = self.get_argument('video_img')
        video_url = self.get_argument('video_url')
        auth_id = self.get_argument('auth_id')
        video_slideshow = self.get_argument('video_slideshow')
        columns_id = self.get_argument('columns_id')
        weight = self.get_argument('weight')
        if not all([name,info]): 
            mes['data'] = "请将带红色*参数填写完整！"
            self.render('../templates/camera/lmicro_add.html',author=author,columns=columns,**mes)
        else:
            try:
                sess.query(Micro_video).filter(Micro_video.name == name).one()
                mes['data'] = "此商品已存在，可添加其他"
                self.render('../templates/camera/lmicro_add.html',author=author, **mes)
            except:
                micro_video = Micro_video(
                    name=name,
                    info=info,
                    video_url=video_url,
                    video_img=video_img,
                    video_slideshow=video_slideshow,
                    column_id=columns_id,
                    auth_id=auth_id,
                    weight=weight
                )
                sess.add(micro_video)
                sess.commit()
                self.redirect('/lmicro')
            else:
                mes['data'] = "未知错误，请重新添加！"
                self.render('../templates/camera/lmicro_add.html',author=author,columns=columns,**mes)


#删除微视频
class Lmicro_del(BaseHandler):
    def get(self, id):
        micro_video = sess.query(Micro_video).filter(Micro_video.id == id).one()
        sess.delete(micro_video)
        sess.commit()
        self.redirect('/lmicro')

#微视频审核
class Lmicro_audit(BaseHandler):
    def get(self,id):
        micro_video = sess.query(Micro_video).filter(Micro_video.id == id).one()
        micro_video.is_show = 1
        sess.commit()
        self.redirect('/lmicro')



#微视频下架
class Lmicro_block(BaseHandler):
    def get(self,id):
        micro_video = sess.query(Micro_video).filter(Micro_video.id == id).one()
        micro_video.is_show = 0
        sess.commit()
        self.redirect('/lmicro')




#编辑微视频
class Lmicro_edit(BaseHandler):
    def get(self, id):
        cookie = self.get_cookie('cookie')
        mes = {}
        mes['data'] = ''
        video = sess.query(Micro_video).filter_by(id=id).first()
        columns = sess.query(Columns).filter(Columns.name=='摄制中心小视频').one()
        author = sess.query(Author).filter(Author.account==cookie).one()
        self.render('../templates/camera/lmicro_edit.html',video=video,author=author,columns=columns,**mes)
    def post(self, id):
        video = sess.query(Micro_video).filter_by(id=id).first()
        name = self.get_argument('name','')
        info = self.get_argument('info','')
        video_img = self.get_argument('video_img')
        video_url = self.get_argument('video_url')
        video_slideshow = self.get_argument('video_slideshow')
        auth_id = self.get_argument('auth_id')
        columns_id = self.get_argument('columns_id')
        weight = self.get_argument('weight')
        video.name = name
        video.info = info
        video.video_img = video_img
        video.video_url = video_url
        video.video_slideshow = video_slideshow
        video.auth_id = auth_id   
        video.column_id = columns_id   
        video.weight = weight
        sess.commit()
        self.redirect('/lmicro')




#微视频详情
class Lmicro_details(BaseHandler):
    def get(self,id):
        video = sess.query(Micro_video).filter(Micro_video.id==id).one()
        author = sess.query(Author.id,Author.name).filter(Author.id==video.auth_id)[0]
        # print(video.column_id)
        video_obj = {}
        video_obj["id"] = video.id
        video_obj["name"] = video.name
        video_obj["info"] = video.info
        video_obj["video_url"] = video.video_url
        video_obj["video_img"] = video.video_img
        video_obj["weight"] = video.weight
        video_obj["video_slideshow"] = video.video_slideshow
        video_obj["amount"] = video.amount
        video_obj["length"] = video.length
        if video.is_show != 0:
            video_obj["is_show"] = "未发布"
        else:
            video_obj["is_show"] = "已发布"
        video_obj["author_id"] = author[0]
        video_obj["author_name"]=author[1]
        video_obj["time"] = video.issue_time
        # print(video_obj)
        self.render('../templates/camera/lmicro_details.html',video_info=video_obj)


# 微视频上传图片
class Lmicro_picture(BaseHandler):
    def get(self,id):
        micro_video = sess.query(Micro_video).filter_by(id=id).first()
        self.render('../templates/camera/lmicro_picture.html', micro_video=micro_video,info = "上传图片")
    def post(self,id):
        micro_video = sess.query(Micro_video).filter_by(id=id).first()
        info = self.get_argument('info')
        url = QINIUURLNAME+info
        try:
            micro_video.video_img = url
            sess.commit()
            self.redirect("/lmicro")
        except:
            self.write('服务器错误')



#微视频上传
class Lmicro_video(BaseHandler):
    def get(self,id):
        micro_video = sess.query(Micro_video).filter_by(id=id).first()
        self.render('../templates/camera/lmicro_video.html',micro_video=micro_video,info = "上传视频")
    def post(self,id):
        micro_video = sess.query(Micro_video).filter_by(id=id).first()
        info = self.get_argument('info')
        url = QINIUURLNAME+info
        try:
            micro_video.video_url = url
            sess.commit()
            self.redirect("/lmicro")
        except:
            self.write('服务器错误')


#摄制中心详情
class Authordetails(BaseHandler):
    def get(self):
        cookie = self.get_cookie('cookie')
        author = sess.query(Author).filter(Author.account==cookie).one()
        video_obj = {}
        video_obj["id"] = author.id
        video_obj["name"] = author.name
        video_obj["info"] = author.info
        video_obj["account"] = author.account
        video_obj["password"] = author.password
        video_obj["img"] = author.img
        video_obj["create_time"] = author.create_time
        self.render('../templates/camera/authordetails.html',video_info=video_obj)


# 微视频上传轮播图
class Lmicro_slideshow(BaseHandler):
    def get(self,id):
        micro_video = sess.query(Micro_video).filter_by(id=id).first()
        self.render('../templates/camera/lmicro_slideshow.html', micro_video=micro_video,info = "上传轮播图")
    def post(self,id):
        micro_video = sess.query(Micro_video).filter_by(id=id).first()
        info = self.get_argument('info')
        url = QINIUURLNAME+info
        try:
            micro_video.video_slideshow = url
            sess.commit()
            self.redirect("/lmicro")
        except:
            self.write('服务器错误')