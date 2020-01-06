from .base import BaseHandler
from models import *
import json
from components.qiniu_upload import upload_file_url,qiniu_up_file  #第一个直接传url即可 第二个需要传文件
import os
import qiniu.config
import logging
from qiniu import Auth,put_data,etag,urlsafe_base64_encode
import time




# 分类管理
class Product_category(BaseHandler):
    def get(self, *args, **kwargs):
        classify = sess.query(Classify).all()
        lens = len(classify)
        self.render('../templates/product_category.html', lens=lens)

    def post(self, *args, **kwargs):
        title = self.get_argument('title', '')
        classify = sess.query(Classify).filter(Classify.name.like('%' + title + '%')).all()
        a = []
        for i in classify:
            b = {}
            b['id'] = i.id
            b['name'] = i.name
            a.append(b)
        str_json = json.dumps(a, indent=2, ensure_ascii=False)
        self.write(str_json)



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
                self.redirect('/product_category_add')
            else:
                 mes['data'] = '此分类已存在，可添加其他'
                 self.render('../templates/product_category_add.html',classify=classify,**mes)



#编辑分类
class Product_category_edit(BaseHandler):
    def get(self, id):
        mes = {}
        mes['data'] = ''
        classifys = sess.query(Classify).filter_by(id=id).first()
        classify = sess.query(Classify).all()
        self.render('../templates/product_category_edit.html',classifys=classifys,classify=classify,**mes)
    def post(self, id):
        classifys = sess.query(Classify).filter_by(id=id).first()
        name = self.get_argument('name','')
        classifys.name = name
        sess.commit()
        self.redirect('/product_category_add')



# 删除分类
class Category_del(BaseHandler):
    def get(self, id):
        classify = sess.query(Classify).filter(Classify.id == id).one()
        sess.delete(classify)
        sess.commit()
        self.redirect('/product_category_add')







# 栏目列表
class Product_column(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('../templates/product_column.html')



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
        if not name:
            mes['data'] = '参数不能为空，请重新输入'
            self.render('../templates/product_column_add.html',columns=columns,**mes)
        else:
            try:
                sess.query(Columns).filter(Columns.name==name).one()
            except:
                columns = Columns(name=name)
                sess.add(columns)
                sess.commit()
                self.redirect('/product_column_add')
            else:
                 mes['data'] = '此分类已存在，可添加其他'
                 self.render('../templates/Product_column_add.html',columns=columns,**mes)



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
        columns.name = name
        sess.commit()
        self.redirect('/product_column_add')



# 栏目上传封面图
class Product_column_picture(BaseHandler):
    def get(self,id):
        columnss = sess.query(Columns).filter_by(id=id).first()
        self.render('../templates/product_column_picture.html', columnss=columnss,info = "上传封面图")
    def post(self,id):
        columnss = sess.query(Columns).filter_by(id=id).first()
        info = self.get_argument('info')
        url = QINIUURLNAME+info
        try:
            columnss.columns_img = url
            sess.commit()
            self.redirect("/product_column_add")
        except:
            self.write('服务器错误')




# 删除栏目
class Column_del(BaseHandler):
    def get(self, id):
        columns = sess.query(Columns).filter(Columns.id == id).one()
        sess.delete(columns)
        sess.commit()
        self.redirect('/product_column_add')





# 标签列表
class Product_label(BaseHandler):
    def get(self, *args, **kwargs):

        self.render('../templates/product_label.html')


# 添加标签
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
        if not name:
            mes['data'] = '参数不能为空，请重新输入'
            self.render('../templates/product_label_add.html',label=label,**mes)
        else:
            try:
                sess.query(Label).filter(Label.name==name).one()
            except:
                label = Label(name=name)
                sess.add(label)
                sess.commit()
                self.redirect('/product_label_add')
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
        label.name = name
        sess.commit()
        self.redirect('/product_label_add')


# 标签上传封面图
class Product_label_picture(BaseHandler):
    def get(self,id):
        label = sess.query(Label).filter_by(id=id).first()
        self.render('../templates/product_label_picture.html', label=label,info = "上传封面图")
    def post(self,id):
        label = sess.query(Label).filter_by(id=id).first()
        info = self.get_argument('info')
        url = QINIUURLNAME+info
        try:
            label.label_img = url
            sess.commit()
            self.redirect("/product_label_add")
        except:
            self.write('服务器错误')



# 删除标签
class Label_del(BaseHandler):
    def get(self, id):
        label = sess.query(Label).filter(Label.id == id).one()
        sess.delete(label)
        sess.commit()
        self.redirect('/product_label_add')