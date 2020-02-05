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



#直播列表
class Sinatv_list(BaseHandler):
    def get(self, *args, **kwargs):
        sinatv = sess.query(Sinatv).all()
        lens = len(sinatv)
        s_list = []
        for info in sinatv:
            item={}
            item["id"] = info.id
            item["name"]=info.name
            item["img"]=info.img
            item["livesrc"]=info.livesrc
            item["weight"]=info.weight
            item["types"]=info.types
            item["is_show"]=info.is_show
            s_list.append(item)
        self.render('../templates/sinatv_list.html', sinatv=s_list, lens=lens)
    def post(self, *args, **kwargs):
        title = self.get_argument('title', '')
        sinatv = sess.query(Sinatv).filter(Sinatv.name.like('%' + title + '%')).all()
        lens = len(sinatv)
        s_list = []
        for info in sinatv:
            item={}
            item["id"] = info.id
            item["name"]=info.name
            item["img"]=info.img
            item["livesrc"]=info.livesrc
            item["weight"]=info.weight
            item["types"]=info.types
            item["is_show"]=info.is_show
            s_list.append(item)
        self.render('../templates/sinatv_list.html', sinatv=s_list, lens=lens)


#添加直播
class Sinatv_add(BaseHandler):
    def get(self,*args,**kwargs):
        mes = {}
        mes['data'] = ''
        self.render('../templates/sinatv_add.html',**mes)
    def post(self, *args, **kwargs):
        mes = {}
        mes['data'] = ''
        name = self.get_argument('name')
        img = self.get_argument('img')
        livesrc = self.get_argument('livesrc')
        weight = self.get_argument('weight')
        types = self.get_argument('types')
        is_show = self.get_argument('is_show')
        if not all([name,weight,is_show]):
            mes['data'] = "请将带红色*参数填写完整！"
            self.render('../templates/sinatv_add.html',**mes)
        else:
            try:
                sess.query(Sinatv).filter(Sinatv.name==name).one()
                mes['data'] = "此直播信息已存在，可添加其他"
                self.render('../templates/sinatv_add.html', **mes)
            except:
                sinatv = Sinatv(
                    name=name,
                    img=img,
                    livesrc=livesrc,
                    weight=weight,
                    types=types,
                    is_show=is_show
                )
                sess.add(sinatv)
                sess.commit()
                self.redirect('/sinatv_list')
            else:
                mes['data'] = "未知错误，请重新添加！"
                self.render('../templates/sinatv_add.html', **mes)

#删除直播
class Sinatv_del(BaseHandler):
    def post(self, id):
        id = int(id)
        sinatv = sess.query(Sinatv).filter(Sinatv.id == id).one()
        sess.delete(sinatv)
        sess.commit()
        return self.write(json.dumps({"status": 200, "msg": "成功！"}, cls=AlchemyEncoder,ensure_ascii=False))



#直播审核
class Sinatv_audit(BaseHandler):
    def get(self,id):
        sinatv = sess.query(Sinatv).filter(Sinatv.id == id).one()
        sinatv.is_show = 0
        sess.commit()
        self.redirect('/sinatv_list')


#直播下架
class Sinatv_block(BaseHandler):
    def get(self,id):
        sinatv = sess.query(Sinatv).filter(Sinatv.id == id).one()
        sinatv.is_show = 1
        sess.commit()
        self.redirect('/sinatv_list')



#编辑公告
class Sinatv_edit(BaseHandler):
    def get(self, id):
        mes = {}
        mes['data'] = ''
        sinatv = sess.query(Sinatv).filter_by(id=id).first()
        self.render('../templates/sinatv_edit.html',sinatv=sinatv,**mes)
    def post(self, id):
        sinatv = sess.query(Sinatv).filter_by(id=id).first()
        name = self.get_argument('name')
        img = self.get_argument('img')
        livesrc = self.get_argument('livesrc')
        weight = self.get_argument('weight')
        types = self.get_argument('types')
        is_show = self.get_argument('is_show')
        sinatv.name = name
        sinatv.img =img
        sinatv.livesrc =livesrc
        sinatv.weight =weight
        sinatv.types =types
        sinatv.is_show = is_show
        sess.commit()
        self.redirect('/sinatv_list')



#直播详情
class Sinatv_details(BaseHandler):
    def get(self,id):
        sinatv = sess.query(Sinatv).filter(Sinatv.id==id).one()
        video_obj = {}
        video_obj["id"] = sinatv.id
        video_obj["name"] = sinatv.name
        video_obj["types"] = sinatv.types
        video_obj["weight"] = sinatv.weight
        video_obj["livesrc"] = sinatv.livesrc
        video_obj["img"] = sinatv.img
        video_obj["create_time"] = sinatv.create_time
        video_obj["is_show"] = sinatv.is_show

        if sinatv.is_show != 0:
            video_obj["is_show"] = "不展示"
        else:
            video_obj["is_show"] = "展示"
        self.render('../templates/sinatv_details.html',video_info=video_obj)



# 直播上传图片
class Sinatv_picture(BaseHandler):
    def get(self,id):
        sinatv = sess.query(Sinatv).filter_by(id=id).first()
        self.render('../templates/sinatv_picture.html', sinatv=sinatv,info = "上传直播图片")
    def post(self,id):
        sinatv = sess.query(Sinatv).filter_by(id=id).first()
        info = self.get_argument('info')
        url = QINIUURLNAME+info
        try:
            sinatv.img = url
            sess.commit()
            return self.write(json.dumps({"status": 200, "msg": "成功"}, cls=AlchemyEncoder,ensure_ascii=False))
        except:
            return self.write(json.dumps({"status": 10010, "msg": "失败"}, cls=AlchemyEncoder,ensure_ascii=False)) 



# #删除直播图片  
class Sinatv_picture_delete(BaseHandler):
    def post(self, id):
        id = int(id)
        sinatv = sess.query(Sinatv).filter_by(id=id).first()
        img = str(sinatv.img)
        a = 'http://qiniu.weiinng.cn/'
        picture = img.replace(a,'') 
        deleteap(picture)
        # print('---删除成功----')
        sinatv.img = ''
        sess.commit()
        return self.write(json.dumps({"status": 200, "msg": "成功！"}, cls=AlchemyEncoder,ensure_ascii=False))




#直播上传视频链接
class Sinatv_video(BaseHandler):
    def get(self,id):
        sinatv = sess.query(Sinatv).filter_by(id=id).first()
        self.render('../templates/sinatv_video.html',sinatv=sinatv,info = "上传直播视频")
    def post(self,id):
        sinatv = sess.query(Sinatv).filter_by(id=id).first()
        info = self.get_argument('info')
        url = QINIUURLNAME+info
        try:
            sinatv.livesrc = url
            sess.commit()
            # print('添加成功')
            return self.write(json.dumps({"status": 200, "msg": "成功"}, cls=AlchemyEncoder,ensure_ascii=False))
        except:
            return self.write(json.dumps({"status": 10010, "msg": "失败"}, cls=AlchemyEncoder,ensure_ascii=False)) 



#删除直播视频链接
class Sinatv_video_delete(BaseHandler):
    def post(self, id):
        id = int(id)
        sinatv = sess.query(Sinatv).filter_by(id=id).first()
        video_src = str(sinatv.livesrc)
        # print(video_src)
        a = 'http://qiniu.weiinng.cn/'
        picture = video_src.replace(a,'') 
        # print(picture)
        deleteap(picture)
        # print('---删除成功----')
        sinatv.livesrc = ''
        sess.commit()
        return self.write(json.dumps({"status": 200, "msg": "成功！"}, cls=AlchemyEncoder,ensure_ascii=False))

