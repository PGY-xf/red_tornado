from .base import BaseHandler
from models import *
import json
from components.qiniu_upload import upload_file_url,qiniu_up_file  #第一个直接传url即可 第二个需要传文件
import os
import qiniu.config
import logging
from qiniu import Auth,put_data,etag,urlsafe_base64_encode
from werkzeug.security import generate_password_hash,check_password_hash
import time


#作者管理
class Author_list(BaseHandler):
    def get(self, *args, **kwargs):
        author = sess.query(Author).all()
        lens = len(author)
        m_list = []
        for i in author:
            item={}
            item["id"] = i.id
            item["name"]=i.name
            item["account"]=i.account
            item["info"]=i.info
            item["img"]=i.img       # 图片
            item["is_activate"] = i.is_activate   
            item["create_time"]=i.create_time
            # try:
            #     classify = sess.query(Classify.id,Classify.name).filter(Classify.id==video.classify_id)
            #     item["classify_id"]=classify[0][0]
            #     item["classify_name"] = classify[0][1]
            # except:
            #     item["classify_id"] = ""
            #     item["classify_name"] = ""
            m_list.append(item)
            # print(m_list[0])
        self.render('../templates/author_list.html', author=m_list, lens=lens)
    def post(self,*args,**kwargs):
        title = self.get_argument('title', '')
        author = sess.query(Author).filter(Author.name.like('%' + title + '%')).all()
        lens = len(author)
        m_list = []
        for i in author:
            item={}
            item["id"] = i.id
            item["name"]=i.name
            item["account"]=i.account
            item["info"]=i.info
            item["img"]=i.img       # 图片
            item["is_activate"] = i.is_activate   
            item["create_time"]=i.create_time
            m_list.append(item)
        self.render('../templates/author_list.html', author=m_list, lens=lens)

#添加作者
class Author_add(BaseHandler):
    def get(self,*args,**kwargs):
        mes = {}
        mes['data'] = ''
        self.render('../templates/author_add.html',**mes)
    def post(self, *args, **kwargs):
        mes = {}
        mes['data'] = ''
        name = self.get_argument('name','')
        account = self.get_argument('account','')
        password = self.get_argument('password','')
        img = self.get_argument('img')
        info = self.get_argument('info')
        is_activate = self.get_argument('is_activate')
        if not all([name,account,info,password]):
            mes['data'] = "请将带红色*参数填写完整！"
            self.render('../templates/author_add.html',**mes)
        else:
            try:
                sess.query(Author).filter(Author.name==name).one()
                mes['data'] = "此商品已存在，可添加其他"
                self.render('../templates/author_add.html', **mes)
            except:
                author = Author(
                    name=name,
                    account=account,
                    password = generate_password_hash(password),
                    img=img,
                    info=info,
                    is_activate=is_activate
                )
                sess.add(author)
                sess.commit()
                self.redirect('/author_list')
            else:
                mes['data'] = "未知错误，请重新添加！"
                self.render('../templates/author_add.html', **mes)



#删除作者
class Author_del(BaseHandler):
    def get(self, id):
        author = sess.query(Author).filter(Author.id == id).one()
        sess.delete(author)
        sess.commit()
        self.redirect('/author_list')


#作者审核通过
class Author_audit(BaseHandler):
    def get(self,id):
        author = sess.query(Author).filter(Author.id == id).one()
        author.is_activate = 1
        sess.commit()
        self.redirect('/author_list')


#作者停用
class Author_block(BaseHandler):
    def get(self,id):
        author = sess.query(Author).filter(Author.id == id).one()
        author.is_activate = 0
        sess.commit()
        self.redirect('/author_list')


#编辑作者
class Author_edit(BaseHandler):
    def get(self, id):
        mes = {}
        mes['data'] = ''
        author = sess.query(Author).filter_by(id=id).first()
        self.render('../templates/author_edit.html',author=author,**mes)
    def post(self, id):
        author = sess.query(Author).filter_by(id=id).first()
        name = self.get_argument('name','')
        account = self.get_argument('account','')
        img = self.get_argument('img')
        info = self.get_argument('info')
        is_activate = self.get_argument('is_activate')
        password = self.get_argument('password')
        author.name = name
        author.account = account
        author.img = img
        author.info = info
        author.is_activate = is_activate
        author.password = generate_password_hash(password)
        sess.commit()
        self.redirect('/author_list')




#作者详情
class Author_details(BaseHandler):
    def get(self,id):
        author = sess.query(Author).filter(Author.id==id).one()

        # classify = sess.query(Classify.id,Classify.name).filter(Classify.id==video.classify_id)[0]
        # print(video.column_id)
        video_obj = {}
        video_obj["id"] = author.id
        video_obj["name"] = author.name
        video_obj["info"] = author.info
        video_obj["account"] = author.account
        video_obj["password"] = author.password
        video_obj["img"] = author.img
        video_obj["create_time"] = author.create_time

        # print(video_obj)
        self.render('../templates/author_details.html',video_info=video_obj)



# 作者上传图片
class Author_picture(BaseHandler):
    def get(self,id):
        author = sess.query(Author).filter_by(id=id).first()
        self.render('../templates/author_picture.html', author=author,info = "上传图片")
    def post(self,id):
        author = sess.query(Author).filter_by(id=id).first()
        info = self.get_argument('info')
        url = QINIUURLNAME+info
        try:
            author.img = url
            sess.commit()
            self.redirect("/author_list")
        except:
            self.write('服务器错误')
