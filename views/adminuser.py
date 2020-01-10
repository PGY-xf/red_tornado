from .base import BaseHandler
from models import *
import json
from func_tools import *

#管理员列表
class Admin_list(BaseHandler):
    def get(self,*args,**kwargs):
        adminlist = sess.query(AdminUser).all()
        nums = len(adminlist)
        self.render("../templates/admin_list.html",adminlist=adminlist,adminlen=nums)
    def post(self,*args,**kwargs):
        title = self.get_argument('title', '')
        adminUser = sess.query(AdminUser).filter(AdminUser.name.like('%' + title + '%')).all()
        lens = len(adminUser)
        pass

#管理员添加等操作
class Admin_add(BaseHandler):
    def get(self, *args, **kwargs):
        mes = {}
        mes['data'] = ''
        self.render("../templates/admin_add.html",**mes)
    def post(self, *args, **kwargs):
        mes = {}
        mes['data'] = ''
        user = self.get_argument("adminName","")
        account = self.get_argument("adminAccount", "")
        password = self.get_argument("password", "")
        role = self.get_argument("adminRole",0)
        if not all([user,account,password,role]):
            mes['data'] = "参数不能为空,请重新输入"
            self.render('../templates/admin_add.html',**mes)
        else:
            try:
                sess.query(AdminUser).filter(AdminUser.name==name).one()
            except:
                adminUser = AdminUser(
                    username=user,account=account,password=password,is_super=role)
                sess.add(adminUser)
                sess.commit()
                self.redirect('/admin_list')
            else:
                mes['data'] = "此商品已存在，可添加其他"
                self.render('../templates/admin_add.html',**mes)


#管理员编辑
class Admin_edit(BaseHandler):
    def get(self,id,*args, **kwargs):
        id = int(id)
        adminuser = sess.query(AdminUser).filter(AdminUser.id==id).one()
        self.render("../templates/admin_edit.html",adminuser=adminuser)
    def post(self,id,*args, **kwargs):
        id = int(id)
        adminuser = sess.query(AdminUser).filter(AdminUser.id == id).one()
        try:
            user = self.get_argument("adminName","")
            account = self.get_argument("adminAccount", "")
            password = self.get_argument("password", "")
            role = self.get_argument("adminRole",0)
            adminuser.username = user
            adminuser.account = account
            adminuser.password = password
            adminuser.is_super = role
            sess.commit()
            self.redirect('/admin_list')
        except:
            self.write("修改失败！")





#管理员删除
class Admin_delete(BaseHandler):
    def get(self,id, *args, **kwargs):
        adminuser = sess.query(AdminUser).filter(AdminUser.id==id).one()
        sess.delete(adminuser)
        sess.commit()
        self.write("删除成功！")



# 角色管理
class Admin_role(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('../templates/admin_role.html')


# 权限管理
class Admin_permission(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('../templates/admin_permission.html')