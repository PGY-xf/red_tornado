# 导入依赖
from sqlalchemy import create_engine         # 创建引擎对象的模块
from sqlalchemy.orm import sessionmaker      # 创建和数据库连接会话
from sqlalchemy import Column,String,Integer,DateTime,ForeignKey,Text,DECIMAL # 内置的创建类的方法属性
from sqlalchemy.ext.declarative import declarative_base # 基础类模块
from sqlalchemy.ext.declarative import DeclarativeMeta  # 解码模块
import json
from datetime import datetime
import pymysql
from config import *

db_url = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, DATABASE)
engine = create_engine(db_url)
pymysql.install_as_MySQLdb()
Session=sessionmaker(bind=engine)
sess=Session()
Base = declarative_base(bind=engine)



class IdBase(object):
    id = Column(Integer, primary_key=True, autoincrement=True)


#管理员用户
class AdminUser(Base,IdBase):
    __tablename__ = "adminuser"
    username = Column(String(60))                #用户名
    account = Column(String(60))                 #账号
    password = Column(String(255))               #密码
    is_super = Column(Integer,default=0)         #是否是超级管理员 0位否1为是
    create_time = Column(DateTime(),default=datetime.now)   #注册时间（精确到秒）



#用户表
class User(Base,IdBase):
    __tablename__ = "user"
    name = Column(String(60),default="")                    #用户名
    password = Column(String(255))                          #密码
    phone = Column(String(11))                              #手机号登录
    email = Column(String(60),default="")                   #邮箱
    user_img = Column(String(255))                          #头像
    age = Column(Integer,default=0)                         #年龄  0为保密  大于则显示
    gender = Column(String(100))                            #性别
    birthplace = Column(String(100),default="")             #地址
    is_member = Column(Integer,default=0)                   #是否会员(会员等级1~9)
    is_activate = Column(Integer, default=0)                #是否激活    0未激活  # 1激活
    create_time = Column(DateTime(),default=datetime.now)   #注册时间（精确到秒）



#作者表
class Author(Base,IdBase):
    __tablename__ = "author"
    name = Column(String(60))                               #昵称
    account = Column(String(60))                            #账号
    password = Column(String(255),default='123456')         #密码
    img = Column(String(255))                               #头像
    info = Column(String(255))                              #信息
    bg_img = Column(String(255))                            #背景图片
    is_activate = Column(Integer,default=0)                 #是否激活  0未审核  1审核
    create_time = Column(DateTime(),default=datetime.now)   #注册时间（精确到秒）


# 微视频表
class Micro_video(Base,IdBase):
    __tablename__ = "micro_video"
    name = Column(String(100))                               #微视频内容标题(必填)
    info = Column(String(255))                               #简介
    video_url = Column(String(255))                          #视频地址
    video_img = Column(String(255))                          #视频封面图
    video_slideshow = Column(String(255))                    #轮播图
    length = Column(String(100))                             #片长
    weight = Column(Integer,default=50)                      #权重越小越靠前（1~99）
    amount = Column(Integer,default=0)                       #播放次数
    is_show = Column(Integer,default=0)                      #发布状态 0未审核  1已审核
    column_id = Column(Integer)                              #栏目id
    auth_id = Column(Integer)                                #作者id
    issue_time = Column(DateTime(),default=datetime.now)     #发布时间（精确到秒）




# 栏目表
class Columns(Base,IdBase):
    __tablename__ = "columns"
    name = Column(String(100))                                  #栏目名称
    columns_img = Column(String(255))                           #栏目封面图
    creation_time = Column(DateTime(),default=datetime.now)     #创建时间（精确到秒）




# 电影表
class Video(Base,IdBase):
    __tablename__ = "video"
    name = Column(String(100))                   #电影名（必填）
    english_name = Column(String(100))           #英文名
    director = Column(String(100),default="")    #导演
    cinemanufacturer = Column(String(100))       #制片人
    length = Column(String(100))                 #片长
    video_img1 = Column(Text)                    #视频封面图
    video_slideshow = Column(Text)               #轮播图
    video_src = Column(Text)                     #视频地址  （必填）
    protagonist = Column(String(100))            #主演
    classify_id = Column(Integer)                #分类id
    column_id = Column(Integer)                  #栏目id
    thiscat_id = Column(Integer)                 #标签id
    tag = Column(String(100))                    #服务标签(‘,’分割)
    scriptwriter = Column(String(100))           #编剧
    release_date = Column(String(100))           #上映时间 
    box_office = Column(String(100))             #票房
    intro = Column(Text)                         #电影简介 （必填）
    year = Column(String(100))                   #制片年份 （必填）
    region = Column(String(100))                 #影片地区 （必填）
    amount = Column(Integer,default=0)           #播放次数
    hot = Column(Integer,default=1)              #热度值
    video_weight = Column(Integer,default=40)    #视频权重（0~99）越小越靠前默认为40
    is_vip = Column(Integer,default=0)           #是否是会员视频 0为否  1为是
    is_selection = Column(Integer,default=0)     #是否为精选 默认为否
    is_show = Column(Integer,default=0)          #0未审核  1已审核
    create_time = Column(DateTime(),default=datetime.now)   #注册时间（精确到秒）



# 分类表
class Classify(Base,IdBase):
    __tablename__ = "classify"
    name = Column(String(60))               # 分类名
    creation_time = Column(DateTime(),default=datetime.now)     #发布时间（精确到秒）




# 标签表
class Label(Base,IdBase):
    __tablename__ = "label"
    name = Column(String(100))                                  #标签名称
    label_img = Column(String(255))                             #标签封面图
    creation_time = Column(DateTime(),default=datetime.now)     #发布时间（精确到秒）



#新表
class Affiche(Base,IdBase):
    __tablename__ = "affiche"
    title = Column(String(100))                                 #标题
    imgsrc = Column(String(255))                                #图片地址
    jumplink = Column(String(255))                              #跳转的链接
    place = Column(Integer,default=0)                           #投放位置
    types = Column(Integer,default=0)                           #类型
    create_time = Column(DateTime(),default=datetime.now)       #创建时间（精确到秒）




# 大V   明星
class Big_V(Base,IdBase):
    __tablename__ = "big_v"
    name = Column(String(60))                   #名字
    english_name = Column(String(60))           #英文名
    year = Column(String(100))                  #生日 
    gender = Column(String(100))                #性别  
    nation = Column(String(100))                #民族              
    nationality = Column(String(255))           #国籍
    big_v_img1 = Column(String(100))            #明星封面图
    big_v_img2 = Column(String(100))            #明星封面图2
    director = Column(String(255))              #出生地
    profession = Column(String(100))            #职业
    region = Column(Text)                       #简介
    graduate_academy = Column(String(255))      #毕业院校
    blood_type = Column(String(255))            #血型
    stature = Column(String(255))               #身高
    weight = Column(String(255))                #体重
    constellation = Column(String(255))         #星座
    main_achievements = Column(String(255))     #主要成就
    in_work = Column(String(500))               #代表作品



# 直播频道
class Sinatv(Base,IdBase):
    __tablename__ = "sinatv"
    name = Column(String(60))                   #名称
    img = Column(Text)                          #直播图片
    livesrc = Column(Text)                      #直播链接
    weight = Column(Integer,default=10)         #权重（0~99）越小越靠前默认为10
    types = Column(Integer,default=0)           #类型 默认0
    is_show = Column(Integer,default=0)         #是否展示  0展示（默认）  1不展示
    create_time = Column(DateTime(),default=datetime.now)     #创建时间




# 评论表
class Comment(Base,IdBase):
    __tablename__ = "comment"
    content = Column(Text)                                   # 内容
    comment_time = Column(DateTime(),default=datetime.now)   # 评论时间（精确到秒）
    inform = Column(Integer,default=0)                       # 举报
    types = Column(Integer,default=0)                        #评论类型,如果为0则是对电影的评论，如果大于0 是追加评论。
    user_id = Column(Integer)                                #用户id
    video_id = Column(Integer)                               #电影id
    micro_video_id = Column(Integer)                         #微视频id
    comment_id = Column(Integer)                             #评论id




#用户收藏表
class Collect(Base,IdBase):
    __tablename__ = "collect"
    user_id = Column(Integer)                                 #用户id
    video_type = Column(Integer)                              #影片类型    0微电影    1电影      
    video_id = Column(Integer)                                #用户关注的影片id
    create_time = Column(DateTime(),default=datetime.now)     #创建时间




#用户关注表
class Attention(Base,IdBase):
    __tablename__ = "attention"
    user_id = Column(Integer)                                   #用户id
    attent_type = Column(Integer)                               #关注的类型id   0作者    1主持人    2栏目
    attent_id = Column(Integer)                                 #基于类型的关注id
    create_time = Column(DateTime(),default=datetime.now)       #创建时间




# 点赞表
class Praise(Base,IdBase):
    __tablename__ = "praise"
    user_id = Column(Integer)                #用户id
    video_id = Column(Integer)               #电影id
    micro_video_id = Column(Integer)         #微视频id
    pratype = Column(Integer)                #点赞类型 1为视频点赞  2为大V点赞




#意见反馈表
class Opinion(Base,IdBase):
    __tablename__ = "opinion"
    title = Column(String(60))      
    user_id = Column(Integer)       #用户id
    types = Column(String(60))      #做出下拉菜单
    body = Column(Text)             #内容
    create_time = Column(DateTime(),default=datetime.now)   #反馈时间（精确到秒）




#系统表
class System(Base):
    __tablename__ = 'system'
    id = Column(Integer, primary_key = True,autoincrement=True)  
    site_name = Column(String(255))                 # 网站名称
    domain_name  = Column(String(255))              # 服务器域名
    describe = Column(Text)                         # 描述
    copyrights = Column(String(255))                # 底部版权信息
    number = Column(Integer,default=0)              # 后台登录失败最大次数
    SMTP_server = Column(String(255))               # SMTP服务器
    SMTP_port = Column(Integer,default=0)           # SMTP 端口
    mail_account = Column(String(255))              # 邮箱帐号
    email_password  = Column(Integer,default=0)     # 邮箱密码
    email_address = Column(String(255))             # 收件邮箱地址
    create_time = Column(DateTime(),default=datetime.now)   #修改时间（精确到秒）


#################

# 广告表 
class Advertising(Base,IdBase):
    __tablename__ = "advertising"
    name = Column(String(100))                                  #广告名称
    advertising_img = Column(String(255))                       #广告图片
    advertising_link = Column(String(255))                      #广告链接
    is_show = Column(Integer,default=0)                         #0未审核  1已审核
    types = Column(Integer,default=0)                           #页面展示  0精选页  1电影页  2电视剧页  3动漫页 
    creation_time = Column(DateTime(),default=datetime.now)     #发布时间（精确到秒）




# 资讯公告表
class Notice(Base,IdBase):
    __tablename__ = "notice"
    name = Column(String(100))                                  #公告名称
    notice_link = Column(String(255))                           #公告链接
    is_show = Column(Integer,default=0)                         #0未审核  1已审核
    types = Column(Integer,default=0)                           #页面展示  0精选页  1电影页  2电视剧页  3动漫页 
    creation_time = Column(DateTime(),default=datetime.now)     #发布时间（精确到秒）






# #订单表
# class Order(Base,IdBase):
#     __tablename__='order'
#     trading_status=Column(Integer,default=0)         #支付状态  0已支付  1未支付 2 退款
#     order_amout=Column(Integer)                      #订单金额
#     payment_generation_time=Column(DateTime(),default=datetime.now)     #订单生成时间
#     outer_traed_number=Column(String(255))           #订单号





# #订单明细表
# class Order_detail(Base,IdBase):
#     __tablename__='order_detail'
#     order=Column(String(255),ForeignKey('order.id'))
#     goods_list=Column(Text)#商品列表
#     shipment_status=Column(Integer,default=0)#配送状态
#     shop_addr=Column(String(255))#收货地址





# #优惠卷表
# class Coupon(Base,IdBase):
#     __tablename__ ='coupon'
#     coupon_name = Column(String(50),unique=True) # 优惠卷码
#     coupon_code = Column(Integer,default=0) #是否使用
#     coupon_time = Column(DateTime,default=datetime.now) #过期时间
#     coupon_price = Column(DECIMAL(2,1)) #折扣




# # 轮播图表
# class Slideshow(Base,IdBase):
#     __tablename__ = 'slideshow'
#     micro_type = Column(Integer)       #微视频id
#     video_id = Column(Integer)              #电影id
#     img_stort = Column(Integer)           #图片顺序(0~4)


def sqlalchemy_json(self):
    obj_dict = self.__dict__
    return dict((key, obj_dict[key]) for key in obj_dict if not key.startswith("_"))
Base.__json__ = sqlalchemy_json



class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:  # 添加了对datetime的处理
                    if isinstance(data, datetime.datetime):
                        fields[field] = data.isoformat()
                    elif isinstance(data, datetime.date):
                        fields[field] = data.isoformat()
                    elif isinstance(data, datetime.timedelta):
                        fields[field] = (datetime.datetime.min + data).time().isoformat()
                    else:
                        fields[field] = None
            # a json-encodable dict
            return fields
        return json.JSONEncoder.default(self, obj)

if __name__ == "__main__":
    #创建表
    Base.metadata.create_all()