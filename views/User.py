from .base import BaseHandler
from models import *
import json
from components.qiniu_upload import upload_file_url,qiniu_up_file  #第一个直接传url即可 第二个需要传文件
import os
import qiniu.config
import logging
from qiniu import Auth,put_data,etag,urlsafe_base64_encode
import time
from func_tools import *



#用户管理
class User_list(BaseHandler):
    def get(self, *args, **kwargs):
        user = sess.query(User).all()
        lens = len(user)
        m_list = []
        for i in user:
            item={}
            item["id"] = i.id
            item['name'] = i.name
            item['phone'] = i.phone
            item['password'] = i.password
            item['gender'] = i.gender
            item['is_member'] = i.is_member
            item["user_img"]=i.user_img       # 图片
            item['email'] = i.email
            item['create_time'] = i.create_time    
            item['is_activate'] = i.is_activate
            # try:
            #     classify = sess.query(Classify.id,Classify.name).filter(Classify.id==video.classify_id)
            #     item["classify_id"]=classify[0][0]
            #     item["classify_name"] = classify[0][1]
            # except:
            #     item["classify_id"] = ""
            #     item["classify_name"] = ""
            m_list.append(item)
            # print(m_list[0])
        self.render('../templates/user_list.html', user=m_list, lens=lens)
    def post(self,*args,**kwargs):
        title = self.get_argument('title', '')
        user = sess.query(User).filter(User.name.like('%' + title + '%')).all()
        lens = len(user)
        m_list = []
        for i in user:
            item={}
            item["id"] = i.id
            item['name'] = i.name
            item['phone'] = i.phone
            item['password'] = i.password
            item['gender'] = i.gender
            item['is_member'] = i.is_member
            item["user_img"]=i.user_img       # 图片
            item['email'] = i.email
            item['create_time'] = i.create_time   
            item['is_activate'] = i.is_activate
            m_list.append(item)
        self.render('../templates/user_list.html', user=m_list, lens=lens)


#添加用户
class User_add(BaseHandler):
    def get(self,*args,**kwargs):
        mes = {}
        mes['data'] = ''
        self.render('../templates/user_add.html',**mes)
    def post(self, *args, **kwargs):
        mes = {}
        mes['data'] = ''
        name = self.get_argument('name','')
        gender = self.get_argument('gender','')
        phone = self.get_argument('phone','') 
        email = self.get_argument('email')
        user_img = self.get_argument('user_img')
        birthplace = self.get_argument('birthplace')
        is_activate = self.get_argument('is_activate')
        if not all([name,phone,email]):
            mes['data'] = "请将带红色*参数填写完整！"
            self.render('../templates/user_add.html',**mes)
        else:
            try:
                sess.query(User).filter(User.name==name).one()
                mes['data'] = "此用户已存在，可添加其他"
                self.render('../templates/user_add.html', **mes)
            except:
                user = User(
                    name=name,
                    gender=gender,
                    email=email,
                    phone=phone,
                    birthplace=birthplace,
                    user_img=user_img,
                    is_activate=is_activate
                )
                sess.add(user)
                sess.commit()
                self.redirect('/user_list')
            else:
                mes['data'] = "未知错误，请重新添加！"
                self.render('../templates/user_add.html', **mes)



#删除用户
class User_del(BaseHandler):
    def post(self, id):
        id = int(id)
        user = sess.query(User).filter(User.id == id).one()
        sess.delete(user)
        sess.commit()
        return self.write(json.dumps({"status": 200, "msg": "成功！"}, cls=AlchemyEncoder,ensure_ascii=False))



#用户停用
class User_audit(BaseHandler):
    def get(self,id):
        user = sess.query(User).filter(User.id == id).one()
        user.is_activate = 1
        sess.commit()
        self.redirect('/user_list')


#用户启用
class User_start(BaseHandler):
    def get(self,id):
        user = sess.query(User).filter(User.id == id).one()
        user.is_activate = 0
        sess.commit()
        self.redirect('/user_list')


#编辑用户
class User_edit(BaseHandler):
    def get(self, id):
        mes = {}
        mes['data'] = ''
        user = sess.query(User).filter_by(id=id).first()
        self.render('../templates/user_edit.html',user=user,**mes)
    def post(self, id):
        user = sess.query(User).filter_by(id=id).first()
        name = self.get_argument('name','')
        gender = self.get_argument('gender','')
        phone = self.get_argument('phone','')
        email = self.get_argument('email')
        user_img = self.get_argument('user_img')
        birthplace = self.get_argument('birthplace')
        is_activate = self.get_argument('is_activate')
        
        user.name = name
        user.gender = gender
        user.phone = phone
        user.email = email
        user.user_img = user_img
        user.birthplace = birthplace
        user.is_activate = is_activate
        sess.commit()
        self.redirect('/user_list')



#修改密码
class User_password(BaseHandler):
    def get(self, id):
        mes = {}
        mes['data'] = ''
        user = sess.query(User).filter_by(id=id).first()
        self.render('../templates/user_password.html',user=user,**mes)
    def post(self,id,*args,**kwargs):
        mes = {}
        mes['data'] = ''
        user = sess.query(User).filter_by(id=id).first()
        password1 = self.get_argument('password1','')
        password2 = self.get_argument('password2','')
        if not all([password1,password2]):
            mes['data'] = "参数不能为空"
            self.render('../templates/user_password.html',user=user,**mes)
        else:
            if password1 == password2:
                if user.password == password1:
                    mes['data'] = "密码跟上传密码重复，请重新输入"
                    self.render('../templates/user_password.html',user=user,**mes)
                else:
                    user.password = password1
                    sess.commit()
                    self.redirect('/user_list')
            else:
                mes['data'] = "两次密码输入不正确，请重新输入"
                self.render('../templates/user_password.html',user=user,**mes)


#用户详情
class User_details(BaseHandler):
    def get(self,id):
        user = sess.query(User).filter(User.id==id).one()

        # classify = sess.query(Classify.id,Classify.name).filter(Classify.id==video.classify_id)[0]
        # print(video.column_id)
        video_obj = {}
        video_obj["id"] = user.id
        video_obj['name'] = user.name
        video_obj['phone'] = user.phone
        video_obj['password'] = user.password
        video_obj['gender'] = user.gender
        video_obj["user_img"]=user.user_img       # 图片
        video_obj['email'] = user.email
        video_obj['create_time'] = user.create_time   
        video_obj['is_activate'] = user.is_activate

        # print(video_obj)
        self.render('../templates/user_details.html',video_info=video_obj)

            

#删除的用户
class User_delete(BaseHandler):
    def get(self):
        mes = {}
        mes['data'] = ''
        user = sess.query(User).filter(User.is_activate == 1).all()
        lens = len(user)
        self.render('../templates/user_delete.html',lens=lens,user=user)



# 用户上传头像
class User_picture(BaseHandler):
    def get(self,id):
        user = sess.query(User).filter_by(id=id).first()
        self.render('../templates/user_picture.html', user=user,info = "上传用户头像")
    def post(self,id):
        user = sess.query(User).filter_by(id=id).first()
        info = self.get_argument('info')
        url = QINIUURLNAME+info
        try:
            user.user_img = url
            sess.commit()
            self.redirect("/user_list")
        except:
            self.write('服务器错误')


#删除用户头像
class User_picture_delete(BaseHandler):
    def post(self, id):
        id = int(id)
        user = sess.query(User).filter_by(id=id).first()
        user_img = str(user.user_img)
        # print(user_img)
        a = 'http://qiniu.weiinng.cn/'
        picture = user_img.replace(a,'') 
        # print(picture)
        deleteap(picture)
        # print('---删除成功----')
        user.user_img = ''
        sess.commit()
        return self.write(json.dumps({"status": 200, "msg": "成功！"}, cls=AlchemyEncoder,ensure_ascii=False))
