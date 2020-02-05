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




# #########  视频logo
# import moviepy.editor as mp

# video = mp.VideoFileClip("./tesst.mp4")
 
# logo = (mp.ImageClip("./央视融媒.jpg")
#         .set_duration(video.duration) # 水印持续时间
#         .resize(height=50) # 水印的高度，会等比缩放
#         .margin(right=8, top=8, opacity=1) # 水印边距和透明度
#         .set_pos(("right","top"))) # 水印的位置

# final = mp.CompositeVideoClip([video, logo])
# # mp4文件默认用libx264编码， 比特率单位bps
# final.write_videofile("test.mp4",audio=False) 



# from moviepy.editor import VideoFileClip

# heve_filename = './tesst.mp4'
# no_filename = './test.mp4'
# def setaudio(heve_filename,no_filename):
#     clip1 = VideoFileClip(heve_filename,audio=True)   ## 读取视频
#     audioclip = clip1.audio                ## 视频声音
#     clip2 = VideoFileClip(no_filename)
#     clip2 = clip2.set_audio(audioclip)
#     clip2.write_videofile('test.mp4')

# setaudio(heve_filename,no_filename)

