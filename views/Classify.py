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



# 分类管理
class Product_category(BaseHandler):
    def get(self, *args, **kwargs):
        classify = sess.query(Classify).all()
        lens = len(classify)
        c_list = []
        for info in classify:
            item={}
            item["id"] = info.id
            item["name"]=info.name
            c_list.append(item)
        self.render('../templates/product_category.html',classify=c_list,lens=lens)
    def post(self,*args,**kwargs):
        title = self.get_argument('title', '')
        classify = sess.query(Classify).filter(Classify.name.like('%' + title + '%')).all()
        lens = len(classify)
        c_list = []
        for info in classify:
            item={}
            item["id"] = info.id
            item["name"]=info.name
            c_list.append(item)
        self.render('../templates/product_category.html', classify=c_list, lens=lens)




# 添加分类
class Product_category_add(BaseHandler):
    def get(self, *args, **kwargs):
        classify = sess.query(Classify).all()
        mes = {}
        mes['data'] = ''
        self.render('../templates/product_category_add.html', classify=classify,**mes)
    def post(self, *args, **kwargs):
        classify = sess.query(Classify).all()
        mes = {}
        name = self.get_argument('name', '')
        if not name:
            mes['data'] = '参数不能为空，请重新输入'
            self.render('../templates/product_category_add.html',classify=classify,**mes)
        else:
            try:
                sess.query(Classify).filter(Classify.name==name).one()
            except:
                classify = Classify(name=name)
                sess.add(classify)
                sess.commit()
                self.redirect('/product_category')
            else:
                 mes['data'] = '此分类已存在，可添加其他'
                 self.render('../templates/product_category_add.html',classify=classify,**mes)



#编辑分类
class Product_category_edit(BaseHandler):
    def get(self, id):
        mes = {}
        mes['data'] = ''
        classifys = sess.query(Classify).filter_by(id=id).first()
        self.render('../templates/product_category_edit.html',classifys=classifys,**mes)
    def post(self, id):
        classifys = sess.query(Classify).filter_by(id=id).first()
        name = self.get_argument('name','')
        classifys.name = name
        sess.commit()
        self.redirect('/product_category')



# 删除分类
class Category_del(BaseHandler):
    def post(self, id):
        id = int(id)
        classify = sess.query(Classify).filter(Classify.id == id).one()
        sess.delete(classify)
        sess.commit()
        return self.write(json.dumps({"status": 200, "msg": "成功！"}, cls=AlchemyEncoder,ensure_ascii=False))






#栏目列表
class Product_column(BaseHandler):
    def get(self,*args,**kwargs):
        columns = sess.query(Columns).all()
        lens = len(columns)
        c_list = []
        for info in columns:
            item={}
            item["id"] = info.id
            item["name"]=info.name
            item["columns_img"]=info.columns_img
            c_list.append(item)
        self.render('../templates/product_column.html',columns=c_list,lens=lens)
    def post(self,*args,**kwargs):
        title = self.get_argument('title', '')
        columns = sess.query(Columns).filter(Columns.name.like('%' + title + '%')).all()
        lens = len(columns)
        c_list = []
        for info in columns:
            item={}
            item["id"] = info.id
            item["name"]=info.name
            item["columns_img"]=info.columns_img
            c_list.append(item)
        self.render('../templates/product_column.html', columns=c_list, lens=lens)


# # 添加栏目
class Product_column_add(BaseHandler):
    def get(self, *args, **kwargs):
        columns = sess.query(Columns).all()
        mes = {}
        mes['data'] = ''
        self.render('../templates/product_column_add.html', columns=columns,**mes)
    def post(self, *args, **kwargs):
        columns = sess.query(Columns).all()
        mes = {}
        name = self.get_argument('name', '')
        columns_img = self.get_argument('columns_img', '')
        if not name:
            mes['data'] = '参数不能为空，请重新输入'
            self.render('../templates/product_column_add.html',columns=columns,**mes)
        else:
            try:
                sess.query(Columns).filter(Columns.name==name).one()
            except:
                columns = Columns(name=name,columns_img=columns_img)
                sess.add(columns)
                sess.commit()
                self.redirect('/product_column')
            else:
                 mes['data'] = '此分类已存在，可添加其他'
                 self.render('../templates/product_column_add.html',columns=columns,**mes)


#编辑栏目
class Product_column_edit(BaseHandler):
    def get(self, id):
        mes = {}
        mes['data'] = ''
        columnss = sess.query(Columns).filter_by(id=id).first()
        columns = sess.query(Columns).all()
        self.render('../templates/product_column_edit.html',columnss=columnss,columns=columns,**mes)
    def post(self, id):
        columns = sess.query(Columns).filter_by(id=id).first()
        name = self.get_argument('name','')
        columns_img = self.get_argument('columns_img', '')
        columns.name = name
        columns.columns_img = columns_img
        sess.commit()
        self.redirect('/product_column')



# 删除栏目
class Product_column_del(BaseHandler):
    def post(self, id):
        id = int(id)
        columns = sess.query(Columns).filter(Columns.id == id).one()
        sess.delete(columns)
        sess.commit()
        return self.write(json.dumps({"status": 200, "msg": "成功！"}, cls=AlchemyEncoder,ensure_ascii=False))





# 栏目上传封面图
class Product_column_picture(BaseHandler):
    def get(self,id):
        columnss = sess.query(Columns).filter_by(id=id).first()
        self.render('../templates/product_column_picture.html', columnss=columnss,info = "上传栏目封面图")
    def post(self,id):
        columnss = sess.query(Columns).filter_by(id=id).first()
        info = self.get_argument('info')
        url = QINIUURLNAME+info
        try:
            columnss.columns_img = url
            sess.commit()
            return self.write(json.dumps({"status": 200, "msg": "成功"}, cls=AlchemyEncoder,ensure_ascii=False))
        except:
            return self.write(json.dumps({"status": 10010, "msg": "失败"}, cls=AlchemyEncoder,ensure_ascii=False)) 


#删除栏目图片
class Column_picture_delete(BaseHandler):
    def post(self, id):
        id = int(id)
        columnss = sess.query(Columns).filter_by(id=id).first()
        columns_img = str(columnss.columns_img)
        # print(columns_img)
        a = 'http://qiniu.weiinng.cn/'
        picture = columns_img.replace(a,'') 
        # print(picture)
        deleteap(picture)
        # print('---删除成功----')
        columnss.columns_img = ''
        sess.commit()
        return self.write(json.dumps({"status": 200, "msg": "成功！"}, cls=AlchemyEncoder,ensure_ascii=False))







# 栏目详情页
class Product_column_details(BaseHandler):
    def get(self,id):
        columnss = sess.query(Columns).filter_by(id=id).first()
        self.render('../templates/product_column_details.html', columnss=columnss,info = "查看封面图")









#标签列表
class Product_label(BaseHandler):
    def get(self,*args,**kwargs):
        label = sess.query(Label).all()
        lens = len(label)
        l_list = []
        for info in label:
            item={}
            item["id"] = info.id
            item["name"]=info.name
            item["label_img"]=info.label_img
            l_list.append(item)
        self.render('../templates/product_label.html', label=l_list, lens=lens)
    def post(self,*args,**kwargs):
        title = self.get_argument('title', '')
        label = sess.query(Label).filter(Label.name.like('%' + title + '%')).all()
        lens = len(label)
        l_list = []
        for info in label:
            item={}
            item["id"] = info.id
            item["name"]=info.name
            item["label_img"]=info.label_img
            l_list.append(item)
        self.render('../templates/product_label.html', label=l_list, lens=lens)




#添加标签
class Product_label_add(BaseHandler):
    def get(self, *args, **kwargs):
        label = sess.query(Label).all()
        mes = {}
        mes['data'] = ''
        self.render('../templates/product_label_add.html', label=label,**mes)
    def post(self, *args, **kwargs):
        label = sess.query(Label).all()
        mes = {}
        name = self.get_argument('name', '')
        label_img = self.get_argument('label_img', '')
        if not name:
            mes['data'] = '参数不能为空，请重新输入'
            self.render('../templates/product_label_add.html',label=label,**mes)
        else:
            try:
                sess.query(Label).filter(Label.name==name).one()
            except:
                label = Label(name=name,label_img=label_img)
                sess.add(label)
                sess.commit()
                self.redirect('/product_label')
            else:
                 mes['data'] = '此分类已存在，可添加其他'
                 self.render('../templates/product_label_add.html',label=label,**mes)




#编辑标签
class Product_label_edit(BaseHandler):
    def get(self, id):
        mes = {}
        mes['data'] = ''
        labels = sess.query(Label).filter_by(id=id).first()
        label = sess.query(Label).all()
        self.render('../templates/product_label_edit.html',label=label,labels=labels,**mes)
    def post(self, id):
        label = sess.query(Label).filter_by(id=id).first()
        name = self.get_argument('name','')
        label_img = self.get_argument('label_img', '')
        label.name = name
        label.label_img = label_img
        sess.commit()
        self.redirect('/product_label')



# 删除标签
class Product_label_del(BaseHandler):
    def post(self, id):
        id = int(id)
        label = sess.query(Label).filter(Label.id == id).one()
        sess.delete(label)
        sess.commit()
        return self.write(json.dumps({"status": 200, "msg": "成功！"}, cls=AlchemyEncoder,ensure_ascii=False))



# 标签上传封面图
class Product_label_picture(BaseHandler):
    def get(self,id):
        label = sess.query(Label).filter_by(id=id).first()
        self.render('../templates/product_label_picture.html', label=label,info = "上传标签封面图")
    def post(self,id):
        label = sess.query(Label).filter_by(id=id).first()
        info = self.get_argument('info')
        url = QINIUURLNAME+info
        try:
            label.label_img = url
            sess.commit()
            return self.write(json.dumps({"status": 200, "msg": "成功"}, cls=AlchemyEncoder,ensure_ascii=False))
        except:
            return self.write(json.dumps({"status": 10010, "msg": "失败"}, cls=AlchemyEncoder,ensure_ascii=False)) 





#删除栏目图片
class Label_picture_delete(BaseHandler):
    def post(self, id):
        id = int(id)
        label = sess.query(Label).filter_by(id=id).first()
        label_img = str(label.label_img)
        print(label_img)
        a = 'http://qiniu.weiinng.cn/'
        picture = label_img.replace(a,'') 
        print(picture)
        deleteap(picture)
        print('---删除成功----')
        label.label_img = ''
        sess.commit()
        return self.write(json.dumps({"status": 200, "msg": "成功！"}, cls=AlchemyEncoder,ensure_ascii=False))






# 标签详情页
class Product_label_details(BaseHandler):
    def get(self,id):
        label = sess.query(Label).filter_by(id=id).first()
        self.render('../templates/product_label_details.html', label=label,info = "查看封面图")
