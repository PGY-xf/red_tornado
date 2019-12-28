from .base import BaseHandler
from models import *
import json
from components.qiniu_upload import upload_file_url,qiniu_up_file  #第一个直接传url即可 第二个需要传文件
import os
import qiniu.config
import logging
from qiniu import Auth,put_data,etag,urlsafe_base64_encode
import time


#电影管理
class Film_list(BaseHandler):
    def get(self, *args, **kwargs):
        videos = sess.query(Video).all()
        lens = len(videos)
        m_list = []
        for video in videos:
            item={}
            item["id"] = video.id
            item["name"]=video.name
            item["director"]=video.director
            item["year"]=video.year
            item["region"]=video.region
            #图片
            item["video_img1"] = video.video_img1
            #链接
            item["video_src"] = video.video_src

            item["is_show"] = video.is_show
            item["director"] = video.director
            try:
                classify = sess.query(Classify.id,Classify.name).filter(Classify.id==video.classify_id)
                item["classify_id"]=classify[0][0]
                item["classify_name"] = classify[0][1]
            except:
                item["classify_id"] = ""
                item["classify_name"] = ""
            m_list.append(item)
            # print(m_list[0])
        self.render('../templates/film_list.html', videos=m_list, lens=lens)
    def post(self, *args, **kwargs):
        title = self.get_argument('title', '')
        videos = sess.query(Video).filter(Video.name.like('%' + title + '%')).all()
        lens = len(videos)
        m_list = []
        for video in videos:
            item={}
            item["id"] = video.id
            item["name"]=video.name
            item["director"]=video.director
            item["year"]=video.year
            item["region"]=video.region
            #图片
            item["video_img1"] = video.video_img1
            #链接
            item["video_src"] = video.video_src

            item["is_show"] = video.is_show
            item["director"] = video.director
            try:
                classify = sess.query(Classify.id,Classify.name).filter(Classify.id==video.classify_id)
                item["classify_id"]=classify[0][0]
                item["classify_name"] = classify[0][1]
            except:
                item["classify_id"] = ""
                item["classify_name"] = ""
            m_list.append(item)
            # print(m_list[0])
        self.render('../templates/film_list.html', videos=m_list, lens=lens)


#添加电影
class Film_add(BaseHandler):
    def get(self,*args,**kwargs):
        mes = {}
        mes['data'] = ''
        classify = sess.query(Classify).all()
        self.render('../templates/film_add.html',classify=classify,**mes)
    def post(self, *args, **kwargs):
        classify = sess.query(Classify).all()
        mes = {}
        mes['data'] = ''
        name = self.get_argument('name','')
        director = self.get_argument('director','')
        year = self.get_argument('year')
        region = self.get_argument('region')
        intro = self.get_argument('intro')
        video_img1 = self.get_argument('video_img1')
        video_src = self.get_argument('video_src')
        classify_id = self.get_argument('classify_id','')
        hot = self.get_argument('hot','')
        is_show = self.get_argument('is_show','')
        if not all([name,director,intro]):
            mes['data'] = "请将带红色*参数填写完整！"
            self.render('../templates/film_add.html',classify=classify,**mes)
        else:
            try:
                sess.query(Video).filter(Video.name==name).one()
                mes['data'] = "此商品已存在，可添加其他"
                self.render('../templates/film_add.html',classify=classify, **mes)
            except:
                video = Video(
                    name=name,
                    director=director,
                    year=year,
                    intro=intro,
                    region = region,
                    video_img1=video_img1,
                    video_src=video_src,
                    classify_id=classify_id,
                    hot=hot,
                    is_show=is_show
                )
                sess.add(video)
                sess.commit()
                self.redirect('/film_list')
            else:
                mes['data'] = "未知错误，请重新添加！"
                self.render('../templates/film_add.html',classify=classify, **mes)


#删除微视频
class Film_del(BaseHandler):
    def get(self, id):
        video = sess.query(Video).filter(Video.id == id).one()
        sess.delete(video)
        sess.commit()
        self.redirect('/film_list')

#电影审核
class Film_audit(BaseHandler):
    def get(self,id):
        video = sess.query(Video).filter(Video.id == id).one()
        video.is_show = 1
        sess.commit()
        self.redirect('/film_list')


#电影下架
class Film_block(BaseHandler):
    def get(self,id):
        video = sess.query(Video).filter(Video.id == id).one()
        video.is_show = 0
        sess.commit()
        self.redirect('/film_list')



#编辑电影
class Film_edit(BaseHandler):
    def get(self, id):
        mes = {}
        mes['data'] = ''
        video = sess.query(Video).filter_by(id=id).first()
        classify = sess.query(Classify).all()
        self.render('../templates/film_edit.html',video=video,classify=classify,**mes)
    def post(self, id):
        video = sess.query(Video).filter_by(id=id).first()
        name = self.get_argument('name','')
        director = self.get_argument('director','')
        year = self.get_argument('year')
        region = self.get_argument('region')
        intro = self.get_argument('intro')
        video_img1 = self.get_argument('video_img1')
        video_src = self.get_argument('video_src')
        classify_id = self.get_argument('classify_id','')
        hot = self.get_argument('hot','')
        is_show = self.get_argument('is_show','')
        video.name = name
        video.director = director
        video.year = year
        video.region = region
        video.intro = intro
        video.video_img1 = video_img1
        video.video_src = video_src
        video.classify_id = classify_id
        video.hot = hot
        video.is_show = is_show
        sess.commit()
        self.redirect('/film_list')




#电影详情
class Film_details(BaseHandler):
    def get(self,id):
        video = sess.query(Video).filter(Video.id==id).one()
        classify = sess.query(Classify.id,Classify.name).filter(Classify.id==video.classify_id)[0]
        # print(video.column_id)
        video_obj = {}
        video_obj["id"] = video.id
        video_obj["name"] = video.name
        video_obj["intro"] = video.intro
        video_obj["video_src"] = video.video_src
        video_obj["video_img1"] = video.video_img1
        video_obj["director"] = video.director
        video_obj["length"] = video.length
        video_obj["hot"] = video.hot

        video_obj["year"] = video.year
        video_obj["region"] = video.region
        video_obj["amount"] = video.amount
        video_obj["is_show"] = video.is_show

        if video.is_show != 0:
            video_obj["is_show"] = "未发布"
        else:
            video_obj["is_show"] = "已发布"
        video_obj["classify_id"] = classify[0]
        video_obj["classify_name"] = classify[1]
        # print(video_obj)
        self.render('../templates/film_details.html',video_info=video_obj)





# 电影上传图片
class Film_picture(BaseHandler):
    def get(self,id):
        video = sess.query(Video).filter_by(id=id).first()
        self.render('../templates/film_picture.html', video=video,info = "上传图片")
    def post(self,id):
        video = sess.query(Video).filter_by(id=id).first()
        info = self.get_argument('info')
        url = QINIUURLNAME+info
        try:
            video.video_img1 = url
            sess.commit()
            self.redirect("/film_list")
        except:
            self.write('服务器错误')


#电影上传视频
class Film_video(BaseHandler):
    def get(self,id):
        video = sess.query(Video).filter_by(id=id).first()
        self.render('../templates/film_video.html',video=video,info = "上传电影")
    def post(self,id):
        video = sess.query(Video).filter_by(id=id).first()
        info = self.get_argument('info')
        url = QINIUURLNAME+info
        try:
            video.video_src = url
            sess.commit()
            print('添加成功')
            self.redirect("/film_list")
        except:
            self.write('服务器错误')