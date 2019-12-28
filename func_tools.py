#导包 导入客户端
'''美国号发送邮件'''
from twilio.rest import Client
def send_datas(to,from_,body):
    #定义短信sid
    account_sid = 'AC929f1e9c0bd7f0f2881c731ab816c238'
    #定义秘钥
    auth_token = 'ce02c6f53eaf2154d654d3ec3c224b66'
    #定义客户端对象 
    client = Client(account_sid,auth_token)

    message = client.messages.create(
    to=to,     # 接受短信的手机号，也就是注册界面验证过的那个自己的手机号，注意 写中国区号  +86
    from_=from_,   # 发送短信的美国手机号  区号 +1
    body=body)

    print(message)




'''redis连接'''
import redis
redis_conn = redis.Redis(host="localhost", port=6379)




from models import *
import time
import datetime
from datetime import timedelta

#所有数目
video = len(sess.query(Video).all())   #电影
micro_video = len(sess.query(Micro_video).all())  #微视频
author = len(sess.query(Author).all())   #摄制中心
user = len(sess.query(User).all())    #用户
adminUser = len(sess.query(AdminUser).all())  #管理员
    #今天创建的数目
today = str(datetime.date.today())
video_now = len(sess.query(Video).filter(Video.create_time.like('%' + today + '%')).all())    #电影
micro_video_now = len(sess.query(Micro_video).filter(Micro_video.issue_time.like('%' + today + '%')).all())   #微视频
author_now = len(sess.query(Author).filter(Author.create_time.like('%' + today + '%')).all())    #摄制中心
user_now = len(sess.query(User).filter(User.create_time.like('%' + today + '%')).all())      ##用户 
adminUser_now = len(sess.query(AdminUser).filter(AdminUser.create_time.like('%' + today + '%')).all())   #管理员
    #昨天创建的数目
today = datetime.date.today()
yesterday = today + datetime.timedelta(days=-1)
dateyest = str(yesterday.isoformat())
video_yesterday = len(sess.query(Video).filter(Video.create_time.like('%' + dateyest + '%')).all())    #电影
micro_video_yesterday = len(sess.query(Micro_video).filter(Micro_video.issue_time.like('%' + dateyest + '%')).all())   #微视频
author_yesterday = len(sess.query(Author).filter(Author.create_time.like('%' + dateyest + '%')).all())    #摄制中心
user_yesterday = len(sess.query(User).filter(User.create_time.like('%' + dateyest + '%')).all())      ##用户 
adminUser_yesterday = len(sess.query(AdminUser).filter(AdminUser.create_time.like('%' + dateyest + '%')).all())   #管理员
    #本周创建的数目 
now = datetime.datetime.now()
#本周日期
today = now
this1 = (now - datetime.timedelta(days=now.weekday())).strftime('%Y-%m-%d')
this2 = (now + datetime.timedelta(days=1-now.weekday())).strftime('%Y-%m-%d')
this3 = (now + datetime.timedelta(days=2-now.weekday())).strftime('%Y-%m-%d')
this4 = (now + datetime.timedelta(days=3-now.weekday())).strftime('%Y-%m-%d')
this5 = (now + datetime.timedelta(days=4-now.weekday())).strftime('%Y-%m-%d')
this6 = (now + datetime.timedelta(days=5-now.weekday())).strftime('%Y-%m-%d')
this7 = (now + datetime.timedelta(days=6-now.weekday())).strftime('%Y-%m-%d')
    #电影
video_week1 = len(sess.query(Video).filter(Video.create_time.like('%' + this1 + '%')).all())    #电影
video_week2 = len(sess.query(Video).filter(Video.create_time.like('%' + this2 + '%')).all())    #电影
video_week3 = len(sess.query(Video).filter(Video.create_time.like('%' + this3 + '%')).all())    #电影
video_week4 = len(sess.query(Video).filter(Video.create_time.like('%' + this4 + '%')).all())    #电影
video_week5 = len(sess.query(Video).filter(Video.create_time.like('%' + this5 + '%')).all())    #电影
video_week6 = len(sess.query(Video).filter(Video.create_time.like('%' + this6 + '%')).all())    #电影
video_week7 = len(sess.query(Video).filter(Video.create_time.like('%' + this7 + '%')).all())    #电影
video_week = video_week1+video_week2+video_week3+video_week4+video_week5+video_week6+video_week7
    #微视频
micro_video_week1 = len(sess.query(Micro_video).filter(Micro_video.issue_time.like('%' + this1 + '%')).all())   #微视频
micro_video_week2 = len(sess.query(Micro_video).filter(Micro_video.issue_time.like('%' + this2 + '%')).all())   #微视频
micro_video_week3 = len(sess.query(Micro_video).filter(Micro_video.issue_time.like('%' + this3 + '%')).all())   #微视频
micro_video_week4 = len(sess.query(Micro_video).filter(Micro_video.issue_time.like('%' + this4 + '%')).all())   #微视频
micro_video_week5 = len(sess.query(Micro_video).filter(Micro_video.issue_time.like('%' + this5 + '%')).all())   #微视频
micro_video_week6 = len(sess.query(Micro_video).filter(Micro_video.issue_time.like('%' + this6 + '%')).all())   #微视频
micro_video_week7 = len(sess.query(Micro_video).filter(Micro_video.issue_time.like('%' + this7 + '%')).all())   #微视频
micro_video_week = micro_video_week1+micro_video_week2+micro_video_week3+micro_video_week4+micro_video_week5+micro_video_week6+micro_video_week7
    #摄制中心
author_week1 = len(sess.query(Author).filter(Author.create_time.like('%' + this1 + '%')).all())    #摄制中心
author_week2 = len(sess.query(Author).filter(Author.create_time.like('%' + this2 + '%')).all())    #摄制中心
author_week3 = len(sess.query(Author).filter(Author.create_time.like('%' + this3 + '%')).all())    #摄制中心
author_week4 = len(sess.query(Author).filter(Author.create_time.like('%' + this4 + '%')).all())    #摄制中心
author_week5 = len(sess.query(Author).filter(Author.create_time.like('%' + this5 + '%')).all())    #摄制中心
author_week6 = len(sess.query(Author).filter(Author.create_time.like('%' + this6 + '%')).all())    #摄制中心
author_week7 = len(sess.query(Author).filter(Author.create_time.like('%' + this7 + '%')).all())    #摄制中心
author_week = author_week1+author_week2+author_week3+author_week4+author_week5+author_week6+author_week7
    ##用户 
user_week1 = len(sess.query(User).filter(User.create_time.like('%' + this1 + '%')).all())      ##用户 
user_week2 = len(sess.query(User).filter(User.create_time.like('%' + this2 + '%')).all())      ##用户 
user_week3 = len(sess.query(User).filter(User.create_time.like('%' + this3 + '%')).all())      ##用户 
user_week4 = len(sess.query(User).filter(User.create_time.like('%' + this4 + '%')).all())      ##用户 
user_week5 = len(sess.query(User).filter(User.create_time.like('%' + this5 + '%')).all())      ##用户 
user_week6 = len(sess.query(User).filter(User.create_time.like('%' + this6 + '%')).all())      ##用户 
user_week7 = len(sess.query(User).filter(User.create_time.like('%' + this7 + '%')).all())      ##用户 
user_week = user_week1+user_week2+user_week3+user_week4+user_week5+user_week6+user_week7
    #管理员
adminUser_week1 = len(sess.query(AdminUser).filter(AdminUser.create_time.like('%' + this1 + '%')).all())   #管理员
adminUser_week2 = len(sess.query(AdminUser).filter(AdminUser.create_time.like('%' + this2 + '%')).all())   #管理员
adminUser_week3 = len(sess.query(AdminUser).filter(AdminUser.create_time.like('%' + this3 + '%')).all())   #管理员
adminUser_week4 = len(sess.query(AdminUser).filter(AdminUser.create_time.like('%' + this4 + '%')).all())   #管理员
adminUser_week5 = len(sess.query(AdminUser).filter(AdminUser.create_time.like('%' + this5 + '%')).all())   #管理员
adminUser_week6 = len(sess.query(AdminUser).filter(AdminUser.create_time.like('%' + this6 + '%')).all())   #管理员
adminUser_week7 = len(sess.query(AdminUser).filter(AdminUser.create_time.like('%' + this7 + '%')).all())   #管理员
adminUser_week = adminUser_week1+adminUser_week2+adminUser_week3+adminUser_week4+adminUser_week5+adminUser_week6+adminUser_week7
    #本月创建的数目 
times = time.strftime("%Y-%m", time.localtime())
video_month = len(sess.query(Video).filter(Video.create_time.like('%' + times + '%')).all())    #电影
micro_video_month = len(sess.query(Micro_video).filter(Micro_video.issue_time.like('%' + times + '%')).all())   #微视频
author_month = len(sess.query(Author).filter(Author.create_time.like('%' + times + '%')).all())    #摄制中心
user_month = len(sess.query(User).filter(User.create_time.like('%' + times + '%')).all())      ##用户 
adminUser_month = len(sess.query(AdminUser).filter(AdminUser.create_time.like('%' + times + '%')).all())   #管理员