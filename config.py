import os

BASE_DIRS = os.path.dirname(__file__)


#参数
options = {
    'port':8000,
}

options_img={
    'port':8001
}



#配置
setting = {
    'static_path':os.path.join(BASE_DIRS,'static'),         # 静态资源
    'template_path':os.path.join(BASE_DIRS,'templates'),    # html页面
    'debug':True,
    # 'autoreload':True  flase
}

#mysql配置
HOSTNAME = '106.13.67.197'   #ip地址
PORT = '3306'                #端口
DATABASE = 'red_dbs'          #数据库名  主库:red_dbs  测试库:zzzz,red_db
USERNAME = 'root'            #账号
PASSWORD = '@weining123'          #密码


#redis配置
REDIS_HOST = '127.0.0.1'    #本地展示地址
REDIS_POST = 6379           


#七牛云配置
ACCESS_KEY = "I4CrykkGIkn6t5ebigiaWZdVURypDGgyAHBSVsvI"    # 您的七牛密匙access_key
SECRET_KEY = "dmAHKa5kXI4Z6XyqiIPQJAuu3zrDHkmXJMrKgden"
BUCKET_NAME = "redinnovation"
QINIU_URL = 'redinnovation.s3-cn-north-1.qiniucs.com'
QINIUURLNAME = "http://qiniu.weiinng.cn/"
'''
{
    "status": 200,
    "info": "success",
    "token": "I4CrykkGIkn6t5ebigiaWZdVURypDGgyAHBSVsvI:4MlqJ37VlttafBLIp5JoVnqgSQA=:eyJzY29wZSI6InJlZGlubm92YXRpb24iLCJkZWFkbGluZSI6MTU3NjM0MDM3OH0="
}
'''



def log_decorator(func):
    def decorator(self,*args,**kwargs):
        cookie = self.get_cookie('cookie')
        ids = self.get_cookie('id')
        print(cookie,ids)
        if not cookie:
            self.redirect('/login')
        else:
            self.render('../templates/index.html',cookie=cookie,ids=ids)
    return decorator



def log_camera(func):
    def decorator(self,*args,**kwargs):
        cookie = self.get_cookie('cookie')
        ids = self.get_cookie('id')
        print(cookie,ids)
        if not cookie:
            self.redirect('/login_camera')
        else:
            self.render('../templates/camera/lindex.html',cookie=cookie,ids=ids)
    return decorator