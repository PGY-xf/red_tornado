from .base import BaseHandler
from models import *
import json
from components.qiniu_upload import upload_file_url,qiniu_up_file  #第一个直接传url即可 第二个需要传文件
import os
import qiniu.config
import logging
from qiniu import Auth,put_data,etag,urlsafe_base64_encode
import time



#明星管理
class Celebrity_list(BaseHandler):
    def get(self, *args, **kwargs):
        big_V = sess.query(Big_V).all()
        lens = len(big_V)
        m_list = []
        for i in big_V:
            item={}
            item["id"] = i.id
            item["name"]=i.name
            item["gender"]=i.gender
            item["nation"]=i.nation
            item["region"]=i.region
            item["big_v_img1"] = i.big_v_img1  #图片
            item["year"] = i.year
            item["profession"] = i.profession
            item["director"] = i.director
            item["nationality"] = i.nationality 
            # try:
            #     classify = sess.query(Classify.id,Classify.name).filter(Classify.id==video.classify_id)
            #     item["classify_id"]=classify[0][0]
            #     item["classify_name"] = classify[0][1]
            # except:
            #     item["classify_id"] = ""
            #     item["classify_name"] = ""
            m_list.append(item)
            # print(m_list[0])
        self.render('../templates/celebrity_list.html', big_V=m_list, lens=lens)
    def post(self,*args,**kwargs):
        title = self.get_argument('title', '')
        big_V = sess.query(Big_V).filter(Big_V.name.like('%' + title + '%')).all()
        lens = len(big_V)
        m_list = []
        for i in big_V:
            item={}
            item["id"] = i.id
            item["name"]=i.name
            item["gender"]=i.gender
            item["nation"]=i.nation
            item["region"]=i.region
            item["big_v_img1"] = i.big_v_img1  #图片
            item["year"] = i.year
            item["profession"] = i.profession
            item["director"] = i.director
            item["nationality"] = i.nationality 
            m_list.append(item)
        self.render('../templates/celebrity_list.html', big_V=m_list, lens=lens)


#添加明星
class Celebrity_add(BaseHandler):
    def get(self,*args,**kwargs):
        mes = {}
        mes['data'] = ''
        self.render('../templates/celebrity_add.html',**mes)
    def post(self, *args, **kwargs):
        mes = {}
        mes['data'] = ''
        name = self.get_argument('name','')
        nationality = self.get_argument('nationality','')
        year = self.get_argument('year')
        nation = self.get_argument('nation')
        region = self.get_argument('region')
        gender = self.get_argument('gender')
        big_v_img1 = self.get_argument('big_v_img1')
        profession = self.get_argument('profession')
        graduate_academy = self.get_argument('graduate_academy','')
        blood_type = self.get_argument('blood_type','')
        stature = self.get_argument('stature','')  
        weight = self.get_argument('weight','')
        director = self.get_argument('director','')
        constellation = self.get_argument('constellation','')
        main_achievements = self.get_argument('main_achievements','')
        in_work = self.get_argument('in_work','')

        if not all([name,gender,nationality,year,nation,region]):
            mes['data'] = "请将带红色*参数填写完整！"
            self.render('../templates/celebrity_add.html',**mes)
        else:
            try:
                sess.query(Big_V).filter(Big_V.name==name).one()
                mes['data'] = "此商品已存在，可添加其他"
                self.render('../templates/celebrity_add.html', **mes)
            except:
                big_v = Big_V(
                    name=name,
                    nationality=nationality,
                    year=year,
                    nation=nation,
                    region = region,
                    stature=stature,
                    gender = gender,
                    big_v_img1=big_v_img1,
                    director=director,
                    profession=profession,
                    graduate_academy=graduate_academy,
                    blood_type=blood_type,
                    weight=weight,
                    constellation=constellation,
                    main_achievements=main_achievements,
                    in_work=in_work
                )
                sess.add(big_v)
                sess.commit()
                self.redirect('/celebrity_list')
            else:
                mes['data'] = "未知错误，请重新添加！"
                self.render('../templates/celebrity_add.html', **mes)



#删除明星
class Celebrity_del(BaseHandler):
    def get(self, id):
        big_v = sess.query(Big_V).filter(Big_V.id == id).one()
        sess.delete(big_v)
        sess.commit()
        self.redirect('/celebrity_list')



#编辑明星
class Celebrity_edit(BaseHandler):
    def get(self, id):
        mes = {}
        mes['data'] = ''
        big_v = sess.query(Big_V).filter_by(id=id).first()
        self.render('../templates/celebrity_edit.html',big_v=big_v,**mes)
    def post(self, id):
        big_v = sess.query(Big_V).filter_by(id=id).first()
        name = self.get_argument('name','')
        nationality = self.get_argument('nationality','')
        year = self.get_argument('year')
        nation = self.get_argument('nation')
        region = self.get_argument('region')
        gender = self.get_argument('gender')
        big_v_img1 = self.get_argument('big_v_img1')
        profession = self.get_argument('profession')
        graduate_academy = self.get_argument('graduate_academy','')
        blood_type = self.get_argument('blood_type','')
        stature = self.get_argument('stature','')  
        weight = self.get_argument('weight','')
        director = self.get_argument('director','')
        constellation = self.get_argument('constellation','')
        main_achievements = self.get_argument('main_achievements','')
        in_work = self.get_argument('in_work','')
        big_v.name = name
        big_v.nationality = nationality
        big_v.year = year
        big_v.nation = nation
        big_v.region = region
        big_v.gender = gender
        big_v.big_v_img1 = big_v_img1
        big_v.profession = profession
        big_v.graduate_academy =graduate_academy
        big_v.blood_type = blood_type
        big_v.stature = stature
        big_v.weight = weight
        big_v.director = director
        big_v.constellation = constellation
        big_v.main_achievements = main_achievements
        big_v.in_work = in_work
        sess.commit()
        self.redirect('/celebrity_list')




#明星详情
class Celebrity_details(BaseHandler):
    def get(self,id):
        big_v = sess.query(Big_V).filter(Big_V.id==id).one()

        # classify = sess.query(Classify.id,Classify.name).filter(Classify.id==video.classify_id)[0]
        # print(video.column_id)
        video_obj = {}
        video_obj["id"] = big_v.id
        video_obj["name"] = big_v.name
        video_obj["nationality"] = big_v.nationality
        video_obj["year"] = big_v.year
        video_obj["nation"] = big_v.nation
        video_obj["region"] = big_v.region
        video_obj["gender"] = big_v.gender
        video_obj["big_v_img1"] = big_v.big_v_img1
        video_obj["profession"] = big_v.profession
        video_obj["graduate_academy"] = big_v.graduate_academy
        video_obj["blood_type"] = big_v.blood_type
        video_obj["stature"] = big_v.stature
        video_obj["weight"] = big_v.weight
        video_obj["director"] = big_v.director
        video_obj["constellation"] = big_v.constellation
        video_obj["main_achievements"] = big_v.main_achievements
        video_obj["in_work"] = big_v.in_work
    
        # print(video_obj)
        self.render('../templates/celebrity_details.html',video_info=video_obj)



# 明星上传图片
class Celebrity_picture(BaseHandler):
    def get(self,id):
        big_v = sess.query(Big_V).filter_by(id=id).first()
        self.render('../templates/celebrity_picture.html', big_v=big_v,info = "上传图片")
    def post(self,id):
        big_v = sess.query(Big_V).filter_by(id=id).first()
        info = self.get_argument('info')
        url = QINIUURLNAME+info
        try:
            big_v.big_v_img1 = url
            sess.commit()
            self.redirect("/celebrity_list")
        except:
            self.write('服务器错误')
