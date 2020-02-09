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


#公告列表
class Notice_list(BaseHandler):
    def get(self, *args, **kwargs):
        notice = sess.query(Notice).all()
        lens = len(notice)
        a_list = []
        for info in notice:
            item={}
            item["id"] = info.id
            item["name"]=info.name
            item["types"]=info.types
            item["notice_link"]=info.notice_link.replace('../../pages/friend-link/common-link?weburl=','')
            item["is_show"]=info.is_show
            a_list.append(item)
        self.render('../templates/notice_list.html', notice=a_list, lens=lens)
    def post(self, *args, **kwargs):
        title = self.get_argument('title', '')
        notice = sess.query(Notice).filter(Notice.name.like('%' + title + '%')).all()
        lens = len(notice)
        a_list = []
        for info in notice:
            item={}
            item["id"] = info.id
            item["name"]=info.name
            item["types"]=info.types
            item["notice_link"]=info.notice_link.replace('../../pages/friend-link/common-link?weburl=','')
            item["is_show"]=info.is_show
            a_list.append(item)
        self.render('../templates/notice_list.html', notice=a_list, lens=lens)


#添加公告
class Notice_add(BaseHandler):
    def get(self,*args,**kwargs):
        mes = {}
        mes['data'] = ''
        self.render('../templates/notice_add.html',**mes)
    def post(self, *args, **kwargs):
        mes = {}
        mes['data'] = ''
        name = self.get_argument('name','')
        types = self.get_argument('types')
        notice_link = self.get_argument('notice_link')
        is_show = self.get_argument('is_show','')
        if not all([name,notice_link,types]):
            mes['data'] = "请将带红色*参数填写完整！"
            self.render('../templates/notice_add.html',**mes)
        else:
            try:
                sess.query(Notice).filter(Notice.name==name).one()
                mes['data'] = "此商品已存在，可添加其他"
                self.render('../templates/notice_add.html', **mes)
            except:
                notice = Notice(
                    name=name,
                    types=types,
                    notice_link="../../pages/friend-link/common-link?weburl="+notice_link,
                    is_show=is_show
                )
                sess.add(notice)
                sess.commit()
                self.redirect('/notice_list')
            else:
                mes['data'] = "未知错误，请重新添加！"
                self.render('../templates/notice_add.html', **mes)


#删除公告
class Notice_del(BaseHandler):
    def post(self, id):
        id = int(id)
        notice = sess.query(Notice).filter(Notice.id == id).one()
        sess.delete(notice)
        sess.commit()
        return self.write(json.dumps({"status": 200, "msg": "成功！"}, cls=AlchemyEncoder,ensure_ascii=False))




#公告审核
class Notice_audit(BaseHandler):
    def get(self,id):
        notice = sess.query(Notice).filter(Notice.id == id).one()
        notice.is_show = 0
        sess.commit()
        self.redirect('/notice_list')


#公告下架
class Notice_block(BaseHandler):
    def get(self,id):
        notice = sess.query(Notice).filter(Notice.id == id).one()
        notice.is_show = 1
        sess.commit()
        self.redirect('/notice_list')


#编辑公告
class Notice_edit(BaseHandler):
    def get(self, id):
        mes = {}
        mes['data'] = ''
        notice = sess.query(Notice).filter_by(id=id).first()
        self.render('../templates/notice_edit.html',notice=notice,**mes)
    def post(self, id):
        notice = sess.query(Notice).filter_by(id=id).first()
        name = self.get_argument('name','')
        types = self.get_argument('types','')
        notice_link = self.get_argument('notice_link')
        is_show = self.get_argument('is_show','')
        notice.name = name
        notice.types =types
        notice.notice_link = "../../pages/friend-link/common-link?weburl="+notice_link
        notice.is_show = is_show
        sess.commit()
        self.redirect('/notice_list')




#删除公告图片  
class Notice_picture_delete(BaseHandler):
    def post(self, id):
        id = int(id)
        notice = sess.query(Notice).filter_by(id=id).first()
        notice_img = str(notice.notice_img)
        # print(notice_img)
        a = 'http://qiniu.weiinng.cn/'
        picture = notice_img.replace(a,'') 
        # print(picture)
        deleteap(picture)
        # print('---删除成功----')
        notice.notice_img = ''
        sess.commit()
        return self.write(json.dumps({"status": 200, "msg": "成功！"}, cls=AlchemyEncoder,ensure_ascii=False))







#公告详情
class Notice_details(BaseHandler):
    def get(self,id):
        notice = sess.query(Notice).filter(Notice.id==id).one()
        video_obj = {}
        video_obj["id"] = notice.id
        video_obj["name"] = notice.name
        video_obj["types"] = notice.types
        video_obj["notice_link"] = notice.notice_link.replace('../../pages/friend-link/common-link?weburl=','')
        video_obj["creation_time"] = notice.creation_time
        video_obj["is_show"] = notice.is_show

        if notice.is_show != 0:
            video_obj["is_show"] = "未发布"
        else:
            video_obj["is_show"] = "已发布"
        # print(video_obj)
        self.render('../templates/notice_details.html',video_info=video_obj)




# 公告上传图片
class Notice_picture(BaseHandler):
    def get(self,id):
        notice = sess.query(Notice).filter_by(id=id).first()
        self.render('../templates/notice_picture.html', notice=notice,info = "上传公告图片")
    def post(self,id):
        notice = sess.query(Notice).filter_by(id=id).first()
        info = self.get_argument('info')
        url = QINIUURLNAME+info
        try:
            notice.notice_img = url
            sess.commit()
            return self.write(json.dumps({"status": 200, "msg": "成功"}, cls=AlchemyEncoder,ensure_ascii=False))
        except:
            return self.write(json.dumps({"status": 10010, "msg": "失败"}, cls=AlchemyEncoder,ensure_ascii=False)) 





#广告列表
class Advertising_list(BaseHandler):
    def get(self, *args, **kwargs):
        advertising = sess.query(Advertising).all()
        lens = len(advertising)
        a_list = []
        for info in advertising:
            item={}
            item["id"] = info.id
            item["name"]=info.name
            item["advertising_img"]=info.advertising_img
            item["advertising_link"]=info.advertising_link.replace('../../pages/friend-link/common-link?weburl=','') 
            item["types"]=info.types
            item["is_show"]=info.is_show
            a_list.append(item)
        self.render('../templates/advertising_list.html', advertising=a_list, lens=lens)
    def post(self, *args, **kwargs):
        title = self.get_argument('title', '')
        advertising = sess.query(Advertising).filter(Advertising.name.like('%' + title + '%')).all()
        lens = len(advertising)
        a_list = []
        for info in advertising:
            item={}
            item["id"] = info.id
            item["name"]=info.name
            item["advertising_img"]=info.advertising_img
            item["advertising_link"]=info.advertising_link.replace('../../pages/friend-link/common-link?weburl=','')
            item["types"]=info.types
            item["is_show"]=info.is_show
            a_list.append(item)
        self.render('../templates/advertising_list.html', advertising=a_list, lens=lens)


#添加广告
class Advertising_add(BaseHandler):
    def get(self,*args,**kwargs):
        mes = {}
        mes['data'] = ''
        self.render('../templates/advertising_add.html',**mes)
    def post(self, *args, **kwargs):
        mes = {}
        mes['data'] = ''
        name = self.get_argument('name','')
        advertising_img = self.get_argument('advertising_img')
        advertising_link = self.get_argument('advertising_link')
        types = self.get_argument('types')
        is_show = self.get_argument('is_show','')
        if not all([name,advertising_link,types]):
            mes['data'] = "请将带红色*参数填写完整！"
            self.render('../templates/advertising_add.html',**mes)
        else:
            try:
                sess.query(Advertising).filter(Advertising.name==name).one()
                mes['data'] = "此商品已存在，可添加其他"
                self.render('../templates/advertising_add.html', **mes)
            except:
                advertising = Advertising(
                    name=name,
                    advertising_img=advertising_img,
                    advertising_link="../../pages/friend-link/common-link?weburl="+advertising_link,
                    is_show=is_show,
                    types=types
                )
                sess.add(advertising)
                sess.commit()
                self.redirect('/advertising_list')
            else:
                mes['data'] = "未知错误，请重新添加！"
                self.render('../templates/advertising_add.html', **mes)


#删除广告
class Advertising_del(BaseHandler):
    def post(self, id):
        id = int(id)
        advertising = sess.query(Advertising).filter(Advertising.id == id).one()
        sess.delete(advertising)
        sess.commit()
        # print("删除成功！")
        return self.write(json.dumps({"status": 200, "msg": "成功！"}, cls=AlchemyEncoder,ensure_ascii=False))




#广告审核
class Advertising_audit(BaseHandler):
    def get(self,id):
        advertising = sess.query(Advertising).filter(Advertising.id == id).one()
        advertising.is_show = 0
        sess.commit()
        self.redirect('/advertising_list')


#广告下架
class Advertising_block(BaseHandler):
    def get(self,id):
        advertising = sess.query(Advertising).filter(Advertising.id == id).one()
        advertising.is_show = 1
        sess.commit()
        self.redirect('/advertising_list')


#编辑广告
class Advertising_edit(BaseHandler):
    def get(self, id):
        mes = {}
        mes['data'] = ''
        advertising = sess.query(Advertising).filter_by(id=id).first()
        self.render('../templates/advertising_edit.html',advertising=advertising,**mes)
    def post(self, id):
        advertising = sess.query(Advertising).filter_by(id=id).first()
        name = self.get_argument('name','')
        advertising_img = self.get_argument('advertising_img','')
        advertising_link = self.get_argument('advertising_link')
        is_show = self.get_argument('is_show','')
        types = self.get_argument('types','')
        advertising.name = name
        advertising.advertising_img = advertising_img
        advertising.advertising_link = "../../pages/friend-link/common-link?weburl="+advertising_link
        advertising.is_show = is_show
        advertising.types = types
        sess.commit()
        self.redirect('/advertising_list')




#删除广告图片  
class Advertising_picture_delete(BaseHandler):
    def post(self, id):
        id = int(id)
        advertising = sess.query(Advertising).filter_by(id=id).first()
        advertising_img = str(advertising.advertising_img)
        # print(advertising_img)
        a = 'http://qiniu.weiinng.cn/'
        picture = advertising_img.replace(a,'') 
        # print(picture)
        deleteap(picture)
        # print('---删除成功----')
        advertising.advertising_img = ''
        sess.commit()
        return self.write(json.dumps({"status": 200, "msg": "成功！"}, cls=AlchemyEncoder,ensure_ascii=False))




#广告详情
class Advertising_details(BaseHandler):
    def get(self,id):
        advertising = sess.query(Advertising).filter(Advertising.id==id).one()
        video_obj = {}
        video_obj["id"] = advertising.id
        video_obj["name"] = advertising.name
        video_obj["advertising_img"] = advertising.advertising_img
        video_obj["advertising_link"] = advertising.advertising_link.replace('../../pages/friend-link/common-link?weburl=','')
        video_obj["creation_time"] = advertising.creation_time
        video_obj["is_show"] = advertising.is_show

        if advertising.is_show != 0:
            video_obj["is_show"] = "未发布"
        else:
            video_obj["is_show"] = "已发布"
        # print(video_obj)
        self.render('../templates/advertising_details.html',video_info=video_obj)




# 广告上传图片
class Advertising_picture(BaseHandler):
    def get(self,id):
        advertising = sess.query(Advertising).filter_by(id=id).first()
        self.render('../templates/advertising_picture.html', advertising=advertising,info = "上传广告图片")
    def post(self,id):
        advertising = sess.query(Advertising).filter_by(id=id).first()
        info = self.get_argument('info')
        url = QINIUURLNAME+info
        try:
            advertising.advertising_img = url
            sess.commit()
            return self.write(json.dumps({"status": 200, "msg": "成功"}, cls=AlchemyEncoder,ensure_ascii=False))
        except:
            return self.write(json.dumps({"status": 10010, "msg": "失败"}, cls=AlchemyEncoder,ensure_ascii=False)) 



# 通知列表
class Feidemo_list(BaseHandler):
    def get(self,*args,**kwargs):
        affiche = sess.query(Affiche).all()
        lens = len(affiche)
        a_list = []
        for info in affiche:
            item={}
            item["id"] = info.id
            item["title"]=info.title
            item["imgsrc"]=info.imgsrc
            item["jumplink"]=info.jumplink.replace('../../pages/friend-link/common-link?weburl=','')
            item["place"]=info.place
            item["types"]=info.types
            item["create_time"]=info.create_time
            a_list.append(item)
        self.render('../templates/000feidemo_list.html',affiche=a_list,lens=lens)
    def post(self,*args,**kwargs):
        title = self.get_argument('title', '')
        affiche = sess.query(Affiche).filter(Affiche.title.like('%' + title + '%')).all()
        lens = len(affiche)
        a_list = []
        for info in affiche:
            item={}
            item["id"] = info.id
            item["title"]=info.title
            item["imgsrc"]=info.imgsrc
            item["jumplink"]=info.jumplink
            item["place"]=info.place
            item["types"]=info.types
            item["create_time"]=info.create_time
            a_list.append(item)
        self.render('../templates/notice_list.html', affiche=a_list, lens=lens)


#删除通知
class Feidemo_del(BaseHandler):
    def post(self, id):
        id = int(id)
        affiche = sess.query(Affiche).filter(Affiche.id == id).one()
        sess.delete(affiche)
        sess.commit()
        return self.write(json.dumps({"status": 200, "msg": "成功！"}, cls=AlchemyEncoder,ensure_ascii=False))
