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



#微视频管理
class Product_micro(BaseHandler):
    def get(self, *args, **kwargs):
        micro_video = sess.query(Micro_video).all()
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
        self.render('../templates/product_micro.html', micro_video=m_list, lens=lens)
    def post(self,*args,**kwargs):
        title = self.get_argument('title', '')
        micro_video = sess.query(Micro_video).filter(Micro_video.name.like('%' + title + '%')).all()
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
        self.render('../templates/product_micro.html', micro_video=m_list, lens=lens)



#添加微视频
class Product_micro_add(BaseHandler):
    def get(self, *args, **kwargs):
        mes = {}
        mes['data'] = ''
        columns = sess.query(Columns).all()
        author = sess.query(Author).filter(Author.account=='yangshi').one()
        self.render('../templates/product_micro_add.html',columns=columns,author=author,**mes)
    def post(self, *args, **kwargs):
        columns = sess.query(Columns).all()
        author = sess.query(Author).filter(Author.account=='yangshi').one()
        mes = {}
        mes['data'] = ''
        name = self.get_argument('name','')
        info = self.get_argument('info','')
        video_img = self.get_argument('video_img')
        video_url = self.get_argument('video_url')
        video_slideshow = self.get_argument('video_slideshow')
        column_id = self.get_argument('columns_id')
        auth_id = self.get_argument('auth_id')
        weight = self.get_argument('weight')
        is_show = self.get_argument('is_show')
        if not all([name,info]):
            mes['data'] = "请将带红色*参数填写完整！"
            self.render('../templates/product_micro_add.html',columns=columns,author=author,**mes)
        else:
            try:
                sess.query(Micro_video).filter(Micro_video.name == name).one()
                mes['data'] = "此商品已存在，可添加其他"
                self.render('../templates/product_micro_add.html',columns=columns,author=author, **mes)
            except:
                micro_video = Micro_video(
                    name=name,
                    info=info,
                    video_url=video_url,
                    video_img=video_img,
                    column_id = column_id,
                    auth_id=auth_id,
                    video_slideshow =video_slideshow,
                    weight=weight,
                    is_show=is_show
                )
                sess.add(micro_video)
                sess.commit()
                self.redirect('/product_micro')
            else:
                mes['data'] = "未知错误，请重新添加！"
                self.render('../templates/product_micro_add.html',columns=columns,author=author, **mes)


#删除微视频
class Product_micro_del(BaseHandler):
    def get(self, id):
        micro_video = sess.query(Micro_video).filter(Micro_video.id == id).one()
        sess.delete(micro_video)
        sess.commit()
        self.redirect('/product_micro')

#微视频审核
class Product_micro_audit(BaseHandler):
    def get(self,id):
        micro_video = sess.query(Micro_video).filter(Micro_video.id == id).one()
        micro_video.is_show = 1
        sess.commit()
        self.redirect('/product_micro')



#微视频下架
class Product_micro_block(BaseHandler):
    def get(self,id):
        micro_video = sess.query(Micro_video).filter(Micro_video.id == id).one()
        micro_video.is_show = 0
        sess.commit()
        self.redirect('/product_micro')




#编辑微视频
class Product_micro_edit(BaseHandler):
    def get(self, id):
        mes = {}
        mes['data'] = ''
        video = sess.query(Micro_video).filter_by(id=id).first()
        columns = sess.query(Columns).all()
        author = sess.query(Author).filter(Author.account=='yangshi').one()
        self.render('../templates/product_micro_edit.html',video=video,columns=columns,author=author,**mes)
    def post(self, id):
        video = sess.query(Micro_video).filter_by(id=id).first()
        name = self.get_argument('name','')
        info = self.get_argument('info','')
        video_img = self.get_argument('video_img')
        video_url = self.get_argument('video_url')
        column_id = self.get_argument('columns_id')
        auth_id = self.get_argument('auth_id')
        weight = self.get_argument('weight')
        video_slideshow = self.get_argument('video_slideshow')
        is_show = self.get_argument('is_show')
        video.name = name
        video.info = info
        video.video_img = video_img
        video.video_slideshow = video_slideshow
        video.video_url = video_url
        video.column_id = column_id
        video.auth_id = auth_id
        video.weight = weight
        video.is_show = is_show
        sess.commit()
        self.redirect('/product_micro')




#微视频详情
class Product_micro_details(BaseHandler):
    def get(self,id):
        video = sess.query(Micro_video).filter(Micro_video.id==id).one()
        column = sess.query(Columns.id,Columns.name).filter(Columns.id==video.column_id)[0]
        author = sess.query(Author.id,Author.name).filter(Author.id==video.auth_id)[0]
        # print(video.column_id)
        video_obj = {}
        video_obj["id"] = video.id
        video_obj["name"] = video.name
        video_obj["info"] = video.info
        video_obj["video_url"] = video.video_url
        video_obj["video_img"] = video.video_img
        video_obj["weight"] = video.weight
        video_obj["amount"] = video.amount
        video_obj["length"] = video.length
        video_obj["video_slideshow"] = video.video_slideshow
        if video.is_show != 0:
            video_obj["is_show"] = "未发布"
        else:
            video_obj["is_show"] = "已发布"
        video_obj["column_id"] = column[0]
        video_obj["column_name"] = column[1]
        video_obj["author_id"] = author[0]
        video_obj["author_name"]=author[1]
        video_obj["time"] = video.issue_time
        # print(video_obj)
        self.render('../templates/product_micro_details.html',video_info=video_obj)

#微视频图片
class Product_micro_picture(BaseHandler):
    def get(self,id):
        micro_video = sess.query(Micro_video).filter_by(id=id).first()
        self.render('../templates/product_micro_picture.html', micro_video=micro_video,info = "上传微视频图片")
    def post(self,id):
        micro_video = sess.query(Micro_video).filter_by(id=id).first()
        info = self.get_argument('info')
        url = QINIUURLNAME+info
        try:
            micro_video.video_img = url
            sess.commit()
            self.redirect("/product_micro")
        except:
            self.write('服务器错误')



#删除微视频图片  
class Micro_picture_delete(BaseHandler):
    def get(self,id):
        micro_video = sess.query(Micro_video).filter_by(id=id).first()
        video_img = str(micro_video.video_img)
        print(video_img)
        a = 'http://qiniu.weiinng.cn/'
        picture = video_img.replace(a,'') 
        print(picture)
        deleteap(picture)
        print('---删除成功----')
        micro_video.video_img = ''
        sess.commit()
        self.redirect("/product_micro")





#微视频视频
class Product_micro_video(BaseHandler):
    def get(self,id):
        micro_video = sess.query(Micro_video).filter_by(id=id).first()
        self.render('../templates/product_micro_video.html',micro_video=micro_video,info = "上传微视频")
    def post(self,id):
        micro_video = sess.query(Micro_video).filter_by(id=id).first()
        info = self.get_argument('info')
        url = QINIUURLNAME+info
        try:
            micro_video.video_url = url
            sess.commit()
            print(url)
            self.redirect("/product_micro")
        except:
            self.write('服务器错误')


#删除微视频视频  
class Micro_video_delete(BaseHandler):
    def get(self,id):
        micro_video = sess.query(Micro_video).filter_by(id=id).first()
        video_url = str(micro_video.video_url)
        print(video_url)
        a = 'http://qiniu.weiinng.cn/'
        picture = video_url.replace(a,'') 
        print(picture)
        deleteap(picture)
        print('---删除成功----')
        micro_video.video_url = ''
        sess.commit()
        self.redirect("/product_micro")




# 微视频上传轮播图
class Product_micro_slideshow(BaseHandler):
    def get(self,id):
        micro_video = sess.query(Micro_video).filter_by(id=id).first()
        self.render('../templates/product_micro_slideshow.html', micro_video=micro_video,info = "上传微视频轮播图")
    def post(self,id):
        micro_video = sess.query(Micro_video).filter_by(id=id).first()
        info = self.get_argument('info')
        url = QINIUURLNAME+info
        try:
            micro_video.video_slideshow = url
            sess.commit()
            self.redirect("/product_micro")
        except:
            self.write('服务器错误')



#删除微视频轮播图
class Micro_slideshow_delete(BaseHandler):
    def get(self,id):
        micro_video = sess.query(Micro_video).filter_by(id=id).first()
        video_slideshow = str(micro_video.video_slideshow)
        print(video_slideshow)
        a = 'http://qiniu.weiinng.cn/'
        picture = video_slideshow.replace(a,'') 
        print(picture)
        deleteap(picture)
        print('---删除成功----')
        micro_video.video_slideshow = ''
        sess.commit()
        self.redirect("/product_micro")