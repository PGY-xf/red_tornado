#多对多查询分类
import random

from models import *


print()


######停用
# <a style="text-decoration:none" onclick="member_stop(this,'10001')" href="javascript:;" title="停用"><i class="Hui-iconfont"></i></a>
# <a style="text-decoration:none"  href="" title="停用"><i class="Hui-iconfont"></i></a>

# #####启用
# <a onclick="admin_start(this,id)" href="javascript:;" title="启用" style="text-decoration:none"><i class="Hui-iconfont"></i></a>
# <a  href="" title="启用" style="text-decoration:none"><i class="Hui-iconfont"></i></a>

# #####编辑
# <a title="编辑" href="javascript:;" onclick="member_edit('编辑','member-add.html','4','','510')" class="ml-5" style="text-decoration:none"><i class="Hui-iconfont"></i></a>
# <a title="编辑" href="" class="ml-5" style="text-decoration:none"><i class="Hui-iconfont"></i></a>

# #####修改密码
# <a style="text-decoration:none" class="ml-5" onclick="change_password('修改密码','change-password.html','10001','600','270')" href="javascript:;" title="修改密码"><i class="Hui-iconfont"></i></a>
# <a style="text-decoration:none" class="ml-5" href="" title="修改密码"><i class="Hui-iconfont"></i></a>

# #####删除
# <a title="删除" href="javascript:;" onclick="member_del(this,'1')" class="ml-5" style="text-decoration:none"><i class="Hui-iconfont"></i></a>
# <a title="删除" href="" class="ml-5" style="text-decoration:none"><i class="Hui-iconfont"></i></a>

# #####还原
# <a style="text-decoration:none" href="javascript:;" onclick="member_huanyuan(this,'1')" title="还原"><i class="Hui-iconfont"></i></a>
# <a style="text-decoration:none" href="" title="还原"><i class="Hui-iconfont"></i></a>

# #####审核
# <a style="text-decoration:none" onclick="article_shenhe(this,'10001')" href="javascript:;" title="审核"><i class="icon Hui-iconfont"></i></a>
# <a style="text-decoration:none"  href="" title="审核"><i class="icon Hui-iconfont"></i></a>

# #####下架
# <a style="text-decoration:none" onclick="article_stop(this,'10001')" href="javascript:;" title="下架"><i class="Hui-iconfont"></i></a>
# <a style="text-decoration:none" href="" title="下架"><i class="Hui-iconfont"></i></a>

# #####发布
# <a style="text-decoration:none" onclick="article_start(this,id)" href="javascript:;" title="发布"><i class="Hui-iconfont"></i></a>
# <a style="text-decoration:none" href="" title="发布"><i class="Hui-iconfont"></i></a>

# #####详情
# <a title="详情" href="javascript:;" onclick="system_log_show(this,'10001')" class="ml-5" style="text-decoration:none"><i class="Hui-iconfont"></i></a>
# <a title="详情" href="" class="ml-5" style="text-decoration:none"><i class="Hui-iconfont"></i></a>



# #判断视频时长
# import os
# import sys
# import xlwt
# from moviepy.editor import VideoFileClip


# videoUrl = 'http://qiniu.weiinng.cn/123456wanghankoucai.mp4'
# def gitBideoTime(videoUrl):
#     try:
#         clip = VideoFileClip(videoUrl)
#         time = clip.duration
#         return int(time)
#     except:
#         return 0

# time = gitBideoTime(videoUrl)
# if time >= 200:
#     print('视频超过2分钟，不能上传')
# else:
#     print(time)


# clip = VideoFileClip(videoUrl)
# time = clip.duration
# print(time)

# from PIL import Image,ImageFont,ImageDraw

# im = Image.open("./央视融媒.jpg").convert('RGBA')
# #新建一个空白图片,尺寸与打开图片一样
# txt=Image.new('RGBA', im.size, (0,0,0,0))
# #设置字体
# fnt=ImageFont.truetype("c:/Windows/Fonts/Tahoma.ttf", 40)
# #操作新建的空白图片>>将新建的图片添入画板
# d=ImageDraw.Draw(txt)
# #在新建的图片上添加字体
# d.text((txt.size[0]-115,txt.size[1]-80), "cnBlogs",font=fnt, fill=(255,255,255,255))
# #合并两个图片
# out=Image.alpha_composite(im, txt)
# out.show()


# ##############图片加文字

# from PIL import Image,ImageFont,ImageDraw

# image = Image.open("./abc.jpg")
# text ='央视融媒.com'
# # 指定要使用的字体和大小；
# font = ImageFont.truetype('C:\Windows\Fonts\simhei.ttf',250)
# layer = image.convert('RGBA') # 将图像转为RGBA图像
# # 生成同等大小的图片
# text_overlay = Image.new('RGBA', layer.size, (255, 255, 255,0))
# image_draw = ImageDraw.Draw(text_overlay) # 画图
# # 获取文本大小
# text_size_x, text_size_y = image_draw.textsize(text, font=font)
# # 设置文本文字位置
# # text_xy = (layer.size[0] - text_size_x,layer.size[1]//8 - text_size_y*2)       #右上角
# # text_xy =(layer.size[0] - text_size_x,layer.size[1] - text_size_y)             #右下角
# # text_xy = (layer.size[0]//2 - text_size_x, layer.size[1]//8 - text_size_y*2)   #左上角
# # text_xy = (layer.size[0]//2 - text_size_x, layer.size[1] - text_size_y)        #左下角
# # 设置文本颜色和透明度和位置
# image_draw.text(text_xy, text, font=font, fill=(255, 255, 255,250))
# #将新生成的图片覆盖到需要加水印的图片上
# after = Image.alpha_composite(layer,text_overlay)
# after.save('im_after.png')


# # ######## 图片加图片logo
# from PIL import Image
# # 需要加水印的图片
# img = Image.open("./abc.jpg")
# # 水印图片
# logo = Image.open("./央视融媒.jpg")
# # 图层  0是宽度，1是高度
# layer = Image.new('RGBA', img.size, (255, 255, 255,0))
# layer.paste(logo,(img.size[0]-logo.size[0],img.size[1]-logo.size[1]))         #右下角
# layer.paste(logo,(img.size[0]-logo.size[0],img.size[1]//8-logo.size[1]))      #右上角
# layer.paste(logo,(img.size[0]//6-logo.size[0],img.size[1]//8-logo.size[1]))   #左上角
# layer.paste(logo,(img.size[0]//6-logo.size[0],img.size[1]-logo.size[1]))      #左下角
# # 覆盖
# img_after = Image.composite(layer, img,layer)
# img_after.show()
# img_after.save('target.jpg')


# from moviepy.editor import VideoFileClip

# heve_filename = './tesst.mp4'
# no_filename = './test.mp4'
# def setaudio(heve_filename,no_filename):
#     clip1 = VideoFileClip(heve_filename,audio=True)   ## 读取视频
#     audioclip = clip1.audio                ## 视频声音
#     clip2 = VideoFileClip(no_filename)
#     clip2 = clip2.set_audio(audioclip)
#     clip2.write_videofile('tests.mp4')


# #########  视频logo
# import moviepy.editor as mp
# def abc(videos,img):
#     video = mp.VideoFileClip(videos)
    
#     logo = (mp.ImageClip(img)
#             .set_duration(video.duration) # 水印持续时间
#             .resize(height=80) # 水印的高度，会等比缩放
#             .margin(right=0, top=0, opacity=0) # 水印边距和透明度
#             .set_pos(("right","top"))) # 水印的位置   ##left左  right右   top上

#     final = mp.CompositeVideoClip([video, logo])
#     # mp4文件默认用libx264编码， 比特率单位bps
#     final.write_videofile("test.mp4",audio=False) 
#     setaudio(videos,'test.mp4')

# abc('./tesst.mp4','./央视融媒.jpg')



# #w微信登录获取code码
# class WXlogin(BaseHandler):
#     def get(self, *args, **kwargs):
#         data = {}
#         appid = 'dads'
#         secret = 'asda'
#         url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
#         params = {
#             'appid':appid,
#             'secret':secret,
#             'code': 'code',
#             'grant_type': 'authorization_code'
#         }
#         response = requests.get(url,params=params)
#         data['code'] = 200
#         data['url'] = response.url
#         self.write(json.dumps(data))



# (r"/wxlogin", Index.WXlogin), 

# import requests

# class WXlogin(BaseHandler):
#     def get(self, *args, **kwargs):
#         data = {}
#         appid = 'wx0b67ef4186f1cc34'
#         secret = '3d9c16586ddb85ccc75cc7b579a4c676'
#         url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
#         params = {
#             'appid':appid,
#             'secret':secret,
#             'code': 'code',
#             'grant_type': 'authorization_code'
#         }
#         response = requests.get(url,params=params)
#         data['code'] = 200
#         data['url'] = response.url
#         self.write(json.dumps(data))

# import requests

# class WXlogin(BaseHandler):
#     def get(self, *args, **kwargs):
#         data = {}
#         appid = 'wx0b67ef4186f1cc34'
#         secret = '3d9c16586ddb85ccc75cc7b579a4c676'
#         code = ''
#         url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
#         params = {
#             'appid':appid,
#             'secret':secret,
#             'code': code,
#             'grant_type': 'authorization_code'
#         }
#         response = requests.get(url,params=params)
#         data['code'] = 200
#         data['url'] = response.url
#         self.write(json.dumps(data))




# 微信登录测试
# class Wxlogin(BaseHandler):
#     appid = 'wx0b67ef4186f1cc34'
#     appsecret = '3d9c16586ddb85ccc75cc7b579a4c676'
#     code = ''
#     state = ''
#     def get_info(self):
#         try:
#             self.code = request.get('code')
#             self.state = request.get("state")
#         except:
#             self.write('获取错误')
#         try:
#             url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
#             params = {
#                 'appid': self.appid,
#                 'secret': self.appsecret,
#                 'code': self.code,
#                 'grant_type': 'authorization_code'
#             }
#             res = requests.get(url, params=params).json()
#             print(res)
#             # access_token = res["access_token"]  # 只是呈现给大家看,可以删除这行
#             # openid = res["openid"]  # 只是呈现给大家看,可以删除这行
#         except:
#             self.write('获取错误')
#         try:
#             user_info_url = 'https://api.weixin.qq.com/sns/userinfo'
#             params = {
#                 'access_token': res["access_token"],
#                 'openid': res["openid"],
#             }
#             res = requests.get(user_info_url, params=params).json()
#             print(res)
#         except:
#             self.write('获取错误')



# from weixin.client import WeixinAPI
# APP_ID = 'your app id'
# APP_SECRET = 'your app secret'
# REDIRECT_URI = 'http://your_domain.com/redirect_uri' # 这里一定要注意 地址一定要加上http/https
# scope = ("snsapi_login", )
# api = WeixinAPI(appid=APP_ID,
#  app_secret=APP_SECRET,
#  redirect_uri=REDIRECT_URI)
# authorize_url = api.get_authorize_url(scope=scope)

# access_token = api.exchange_code_for_access_token(code=code)



# api = WeixinAPI(appid=APP_ID,
#  app_secret=APP_SECRET,
#  redirect_uri=REDIRECT_URI)
# # 刷新或续期access_token使用
# refresh_token = api.exchange_refresh_token_for_access_token(refresh_token=auth_info['refresh_token'])
# api = WeixinAPI(access_token=auth_info['access_token'])
# # 获取用户个人信息
# user = api.user(openid=auth_info['openid'])
# # 检查access_token有效性
# v = api.validate_token(openid=auth_info['openid'])