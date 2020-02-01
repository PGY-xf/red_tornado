import re
from .base import BaseHandler
from models import *
import requests
import json
from func_tools import *
from werkzeug.security import generate_password_hash, check_password_hash

access_key = ACCESS_KEY  # AK
secret_key = SECRET_KEY  # SK
bucket_name = BUCKET_NAME  # name
url = QINIU_URL  # url



def auto_rollback(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            sess.rollback()
            sess.error(err)
            raise err
    return wrapper


class GetToken(BaseHandler):
    def get(self, *args, **kwargs):
        # 需要填写你的 Access Key 和 Secret Key
        access_key = ACCESS_KEY
        secret_key = SECRET_KEY
        # 构建鉴权对象
        q = Auth(access_key, secret_key)
        # 要上传的空间
        bucket_name = BUCKET_NAME
        # 上传后保存的文件名
        key = 'token'
        # 生成上传 Token，可以指定过期时间等
        # 上传策略示例
        # https://developer.qiniu.com/kodo/manual/1206/put-policy
        domain = "http://q2cbcbetl.bkt.clouddn.com/"
        policy = {
            'callbackUrl': 'https://requestb.in/1c7q2d31',
            'callbackBody': 'filename=$(fname)&filesize=$(fsize)',
            'persistentOps': 'imageView2/1/w/200/h/200'
        }
        # 3600为token过期时间，秒为单位。3600等于一小时
        token = q.upload_token(bucket_name, key, 3600, policy)
        print("有人取走了token")
        self.write(json.dumps({"uptoken": token, "domain": domain}, ensure_ascii=False))


# 七牛云token
class QiNiuHandler(BaseHandler):
    async def get(self):
        q = Auth('E2IZM3koC1GR1DUqJHactmixzdyZZhx0edBKqDsk', 'GDnMkvRoE_kFhCSuvdqQj0VcNsRDOHzYJJ_bVd0_')
        token = q.upload_token('redinnovation')
        print("有人过来取走了token")
        self.write(json.dumps({'uptoken': token}, ensure_ascii=False))


# 爱看页面的小视频 ID 必须为1
class gitVideolist(BaseHandler):
    @auto_rollback
    def get(self, id, *args, **kwargs):
        id = int(id)
        microall = sess.query(Micro_video).filter(Micro_video.video_url != None,Micro_video.column_id==1,Micro_video.is_show==1,Micro_video.video_img != "",Micro_video != None).all()[id:id + 10]
        video_list = []
        for micro in microall:
            item = {}
            item["id"] = micro.id
            item["title"] = micro.name
            item["playnum"] = micro.amount
            item["video_img"] = micro.video_img
            item["video_url"] = micro.video_url
            item["length"] = ""
            author = sess.query(Author.id, Author.name, Author.img).filter(Author.id == micro.auth_id)
            item["column_id"] = author[0][0]
            item["column_name"] = author[0][1]
            item["column_img"] = author[0][2]
            video_list.append(item)
        return self.write(json.dumps({"status": 200, "msg": "返回成功", 'video_list': video_list}, cls=AlchemyEncoder,
                                     ensure_ascii=False))


# 主页栏目的四个视频
class gitColumnsVideofourList(BaseHandler):
    @auto_rollback
    def get(self, *args, **kwargs):
        listitem = []
        columns = sess.query(Columns).all()
        for col in columns:
            item = {}
            item["colums_id"] = col.id
            item["headerTitle"] = col.name
            item["bodyList"] = []
            microall = sess.query(Micro_video).filter(Micro_video.video_url != None, Micro_video.is_show == 1,
                                                      Micro_video.column_id == col.id).all()
            for vid in microall:
                videoobj = {}
                videoobj["id"] = vid.id
                videoobj["title"] = vid.name
                videoobj["info"] = vid.info
                videoobj["img"] = vid.video_img
                videoobj["video_url"] = vid.video_url
                videoobj["lookNum"] = vid.amount
                videoobj["isHot"] = "true"
                item["bodyList"].append(videoobj)
            listitem.append(item)
        return self.write(json.dumps({"status": 200, "msg": "返回成功", 'columnsVideoList': listitem}, cls=AlchemyEncoder,
                                     ensure_ascii=False))


# APP获取验证码
class App_getverification(BaseHandler):
    def post(self, *args, **kwargs):
        code_type = self.get_argument("code_type")
        # 先判断是那边调取的验证码，然后再去做事情。
        if code_type == "reg":
            phone = self.get_argument("phoneno")
            # 判断用户是否输入了手机号
            isphone = re.match('^1[3,5,7,8,9]\d{9}$', phone)
            if isphone:
                # 判断次手机号是否已经注册
                user = sess.query(User).filter(User.phone == phone).first()
                # 如果user不存在则进行注册：
                if not user:
                    # 生成验证并将验证码发送到用户手机号上！
                    phone = phone
                    # 调用发送验证码的函数
                    set_code_toRedis(code_type, phone)
                    return self.write(
                        json.dumps({"status": 200, "msg": "验证码"}, cls=AlchemyEncoder,
                                   ensure_ascii=False))
                # 如果存在则提醒已注册
                else:
                    return self.write(
                        json.dumps({"status": 200, "msg": "手机号已注册！"}, cls=AlchemyEncoder,
                                   ensure_ascii=False))
            # 手机号格式错误
            else:
                return self.write(
                    json.dumps({"status": 201, "msg": "手机号格式错误。"}, cls=AlchemyEncoder, ensure_ascii=False))
        else:
            return self.write(
                json.dumps({"status": 201, "msg": "缺少验证码类型"}, cls=AlchemyEncoder, ensure_ascii=False))


# 发送验证码
def set_code_toRedis(code_type, phone):
    try:
        phone = phone
        code_type = code_type
        code = ''.join(str(i) for i in random.sample(range(0, 9), 4))  # 随机数
        send_data(to=str(phone), body=code)
        redis_conn.hset(code_type, phone, code)  # 设置过期时间为2分钟
        redis_conn.expire(code_type, 120)
        return "200"
    except:
        return "400"


# APP账号注册
class App_register_user(BaseHandler):
    @auto_rollback
    def post(self, *args, **kwargs):
        phone = self.get_argument("phoneno")
        print("手机号为{}的用户申请注册".format(phone))
        password = self.get_argument("password")
        code = self.get_argument("code")
        invitation = self.get_argument("invitation")
        # 不需要做对手机号重复的判断，只需要对验证码进行判断。
        # 拿到验证码之后去缓存库中判断，以key：手机号  val:验证码
        iscode = redis_conn.hget("reg", phone).decode()
        print(iscode)
        if iscode == code:
            add_user = User(phone=phone, password=generate_password_hash(password), name=phone,
                            user_img="/static/common/default_userimg.jpg")
            sess.add(add_user)
            sess.commit()
            return self.write(
                json.dumps({"status": 200, "msg": "注册成功快去登录把！"}, cls=AlchemyEncoder,
                           ensure_ascii=False))
        else:
            return self.write(
                json.dumps({"status": 201, "msg": "验证码错误！"}, cls=AlchemyEncoder,
                           ensure_ascii=False))


# APP账号登录
class App_login_user(BaseHandler):
    @auto_rollback
    def post(self, *args, **kwargs):
        phone = self.get_argument("phoneno")
        password = self.get_argument("password")
        user_info = sess.query(User).filter(User.phone == phone).one()
        if user_info:
            if check_password_hash(user_info.password, password):
                item = {}
                item["id"] = user_info.id
                item["mobile"] = user_info.phone
                if user_info.name != "" and user_info.name != None:
                    item["nickname"] = user_info.name
                else:
                    item["nickname"] = user_info.phone + "用户"
                item["portrait"] = user_info.user_img
                item["userHistoryList"] = []
                return self.write(
                    json.dumps({"status": 200, "msg": "登录成功！", "user_info": item}, cls=AlchemyEncoder,
                               ensure_ascii=False))
            else:
                return self.write(
                    json.dumps({"status": 200, "msg": "密码错误"}, cls=AlchemyEncoder,
                               ensure_ascii=False))
        else:
            return self.write(
                json.dumps({"status": 200, "msg": "用户不存在"}, cls=AlchemyEncoder,
                           ensure_ascii=False))


# 用户修改密码
class APP_user_update_password(BaseHandler):
    @auto_rollback
    def post(self, *args, **kwargs):
        userid = self.get_argument("userid")
        oldpassword = self.get_argument("oldpassword")
        newpassword = self.get_argument("newpassword")
        useruppassword = sess.query(User).filter(User.id == userid).one()
        if useruppassword:
            if useruppassword.password == oldpassword:
                useruppassword.password = newpassword
                sess.commit()
                return self.write(
                    json.dumps({"status": 200, "msg": "密码修改成功！"}, cls=AlchemyEncoder,
                               ensure_ascii=False))
            else:
                return self.write(
                    json.dumps({"status": 200, "msg": "旧密码输入错误！"}, cls=AlchemyEncoder,
                               ensure_ascii=False))
        else:
            return self.write(
                json.dumps({"status": 201, "msg": "出了点问题请稍后重试！"}, cls=AlchemyEncoder,
                           ensure_ascii=False))


# 获取主持人列表
class getIndexCompere_list(BaseHandler):
    @auto_rollback
    def get(self, *args, **kwargs):
        mingxing_info = sess.query(Big_V).order_by(-Big_V.id).all()
        pro_list = []
        for info in mingxing_info:
            item = {}
            item["id"] = info.id
            item["name"] = info.name
            item["english_name"] = info.english_name
            item["year"] = info.year
            item["gender"] = info.gender
            item["nation"] = info.nation
            item["nationality"] = info.nationality
            item["big_v_img1"] = info.big_v_img1
            item["big_v_img2"] = info.big_v_img2
            item["director"] = info.director
            item["profession"] = info.profession
            item["region"] = info.region
            item["graduate_academy"] = info.graduate_academy
            item["blood_type"] = info.blood_type
            item["stature"] = info.stature
            item["blood_type"] = info.blood_type
            item["weight"] = info.weight
            item["constellation"] = info.constellation
            item["main_achievements"] = info.main_achievements.split('、')
            item["in_work"] = info.in_work.split('、')

            item["profession"] = info.profession.split('、')
            for pro in item["profession"]:
                if pro == "主持人":
                    pro_list.append(item)
                else:
                    pass
        return self.write(
            json.dumps({"status": 200, "msg": "返回成功", "zhuchiren_list": pro_list[:10]}, cls=AlchemyEncoder,
                       ensure_ascii=False))


# 明星详情页
class getIndexCompere_particulars(BaseHandler):
    @auto_rollback
    def get(self, id, *args, **kwargs):
        id = int(id)
        mingxing_info = sess.query(Big_V).filter(Big_V.id == id).one()
        item = {}
        item["id"] = mingxing_info.id
        item["name"] = mingxing_info.name
        item["english_name"] = mingxing_info.english_name
        item["year"] = mingxing_info.year
        item["gender"] = mingxing_info.gender
        item["nation"] = mingxing_info.nation
        item["nationality"] = mingxing_info.nationality
        item["big_v_img1"] = mingxing_info.big_v_img1
        item["big_v_img2"] = mingxing_info.big_v_img2
        item["director"] = mingxing_info.director
        item["profession"] = mingxing_info.profession
        item["region"] = mingxing_info.region
        item["graduate_academy"] = mingxing_info.graduate_academy
        item["blood_type"] = mingxing_info.blood_type
        item["stature"] = mingxing_info.stature
        item["blood_type"] = mingxing_info.blood_type
        item["weight"] = mingxing_info.weight
        item["constellation"] = mingxing_info.constellation
        item["main_achievements"] = mingxing_info.main_achievements.split('、')
        item["in_work"] = mingxing_info.in_work.split('、')
        item["profession"] = mingxing_info.profession.split('、')
        return self.write(
            json.dumps({"status": 200, "msg": "返回成功", "zhuchiren_info": item}, cls=AlchemyEncoder,
                       ensure_ascii=False))


# 主页-电影-视频列表
class getIndexfilm_videolist(BaseHandler):
    @auto_rollback
    def get(self, *args, **kwargs):
        # id 名字  视频图片  播放次数  热度
        videoinfoList = []
        videoObj = sess.query(Video.id, Video.name, Video.video_img1, Video.amount, Video.hot, Video.intro).filter(
            Video.video_src != None, Video.is_show == 1, Video.video_img1 != None,Video.video_img1 != "").all()
        for videoinfo in videoObj:
            item = {}
            item["id"] = videoinfo[0]
            item["title"] = videoinfo[1]
            item["img"] = videoinfo[2]
            item["lookNum"] = videoinfo[3] + 3000
            if videoinfo[4] > 5:
                item["isHot"] = True
            else:
                item["isHot"] = False
            item["info"] = videoinfo[5][:13] + "..."
            videoinfoList.append(item)
            # print(item)
        return self.write(
            json.dumps({"status": 200, "msg": "返回成功", "filmvideolist": videoinfoList}, cls=AlchemyEncoder,
                       ensure_ascii=False))


# 栏目列表
class getIndexColumnsList(BaseHandler):
    @auto_rollback
    def get(self, *args, **kwargs):
        # 展示栏目但不展示不带图片的
        columns = sess.query(Columns).filter(Columns.columns_img != "", Columns.columns_img != None).all()
        column_list = []
        for info in columns:
            item = {}
            item["id"] = info.id
            item["name"] = info.name
            item["columns_img"] = info.columns_img
            column_list.append(item)
        return self.write(
            json.dumps({"status": 200, "msg": "返回成功", "column_list": column_list[:10]}, cls=AlchemyEncoder,
                       ensure_ascii=False))


# 获取图片的主色
import colorsys
def get_dominant_color(image):
    # 颜色模式转换，以便输出rgb颜色值
    image = image.convert('RGBA')
    # 生成缩略图，减少计算量，减小cpu压力
    image.thumbnail((200, 200))
    max_score = 0  # 原来的代码此处为None
    dominant_color = 0  # 原来的代码此处为None，但运行出错，改为0以后
    # 运行成功，原因在于在下面的
    # score > max_score的比较中，max_score的初始格式不定
    for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
        # 跳过纯黑色
        if a == 0:
            continue
        saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
        y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
        y = (y - 16.0) / (235 - 16)
        # 忽略高亮色
        if y > 0.9:
            continue
        score = (saturation + 0.1) * count
        if score > max_score:
            max_score = score
            dominant_color = (r, g, b)
    return dominant_color



# 栏目列表
class getAPP_IndexColumns_info(BaseHandler):
    @auto_rollback
    def post(self, *args, **kwargs):
        column_id = self.get_argument("id", 0)
        id = int(column_id)
        if id > 0:
            column_info = sess.query(Columns.id, Columns.name, Columns.columns_img).filter(Columns.id == id).one()
            item = {}
            item["id"] = column_info[0]
            item["title"] = column_info[1]
            item["titlepic"] = column_info[2]
            item["totalnum"] = "615113"
            item["todaynum"] = "5156"
            item["desc"] = "欢迎观看" + column_info[1] + "的作品"
            item["colnum_videolist"] = []
            item["colnum_new_videolist"] = []
            microall = sess.query(Micro_video.id, Micro_video.name, Micro_video.video_img).filter(
                Micro_video.is_show == 0,
                Micro_video.video_url != None,
                Micro_video.video_url != "",
                Micro_video.video_img != None,
                Micro_video.video_url != "",
                Micro_video.column_id ==
                column_info[0]).all()[:5]
            for video in microall:
                video_item = {}
                video_item["id"] = video[0]
                video_item["title"] = video[1]
                video_item["video_img"] = video[2]
                item["colnum_videolist"].append(video_item)
            new_microall = sess.query(Micro_video.id, Micro_video.name, Micro_video.video_img).filter(
                Micro_video.is_show == 0, Micro_video.video_url != None, Micro_video.video_url != "",
                Micro_video.video_img != None, Micro_video.video_url != "",
                Micro_video.column_id == column_info[0]).order_by(-Micro_video.issue_time).all()[:5]
            for new_video in new_microall:
                new_video_item = {}
                new_video_item["id"] = new_video[0]
                new_video_item["title"] = new_video[1]
                new_video_item["video_img"] = new_video[2]
                item["colnum_new_videolist"].append(new_video_item)
            return self.write(
                json.dumps({"status": 200, "msg": "返回成功", "column_info_obj": item}, cls=AlchemyEncoder,
                           ensure_ascii=False))
        else:
            return self.write(
                json.dumps({"status": 201, "msg": "返回成功"}, cls=AlchemyEncoder,
                           ensure_ascii=False))


# 视频详情页
class get_app_common_video_particulars(BaseHandler):
    @auto_rollback
    def post(self, *args, **kwargs):
        video_id = self.get_argument("video_id", 0)
        id = int(video_id)
        if id > 0:
            info = sess.query(Micro_video.id, Micro_video.name, Micro_video.video_url, Columns.id, Columns.name,
                              Author.id,
                              Author.name, Author.img).join(Columns, Columns.id == Micro_video.column_id).join(Author,
                                                                                                               Author.id == Micro_video.auth_id).filter(
                Micro_video.id == id).one()
            item = {}
            item["id"] = info[0]
            item["video_name"] = info[1]
            item["video_src"] = info[2]
            item["columns_id"] = info[3]
            item["columns_name"] = info[4]
            item["author_id"] = info[5]
            item["author_name"] = info[6]
            item["author_img"] = info[7]
            item["is_comment"] = 1
            return self.write(
                json.dumps({"status": 200, "msg": "返回成功", "info_item": item}, cls=AlchemyEncoder,
                           ensure_ascii=False))
        else:
            return self.write(
                json.dumps({"status": 201, "msg": "失败"}, cls=AlchemyEncoder,
                           ensure_ascii=False))
#主页下推荐栏-反腐倡廉
class get_app_index_four_video(BaseHandler):
    @auto_rollback
    def get(self, *args, **kwargs):
        datainfo = sess.query(Micro_video.id, Micro_video.name, Micro_video.info, Micro_video.video_img).filter(
            Micro_video.column_id == 8).order_by(-Micro_video.id).limit(4).all()
        datalist = []
        for value in datainfo:
            item = {}
            item["id"] = value[0]
            item["title"] = value[1]
            item["info"] = value[2]
            item["img"] = value[3]
            item["isHot"] = True
            datalist.append(item)
        return self.write(
            json.dumps({"status": 200, "msg": "返回成功", "datalist":datalist}, cls=AlchemyEncoder,
                       ensure_ascii=False))

#电影详情页
class get_app_common_movie_particulars(BaseHandler):
    @auto_rollback
    def post(self, *args, **kwargs):
        movie_id = self.get_argument("movie_id",0)
        if movie_id ==0:
            return self.write(
                json.dumps({"status":404, "msg": "找不到页面"}, cls=AlchemyEncoder,
                           ensure_ascii=False))
        else:
            try:
                movie_id = int(movie_id)
                movieinfo = sess.query(Video).filter(Video.id == movie_id, Video.video_src != "",
                                                     Video.video_src != None).one()
                item = {}
                item["id"] = movieinfo.id
                item["title"] = movieinfo.name
                item["info"] = movieinfo.intro
                item["videosrc"] = movieinfo.video_src
                item["tag"] = movieinfo.tag.split('、')
                celebritylist = []
                celebritylist.extend(movieinfo.director.split('、'))
                celebritylist.extend(movieinfo.protagonist.split('、'))
                item["celebrity"] = celebritylist
                item["tuijian"] = []
                if movieinfo.thiscat_id:
                    tuijianlist = sess.query(Video.id, Video.name, Video.video_img1).filter(
                        Video.thiscat_id == movieinfo.thiscat_id, Video.video_img1 != "", Video.video_img1 != None,
                        Video.video_src != "", Video.video_src != None, Video.id != movieinfo.id).order_by(
                        -Video.id).limit(5).all()
                    for info in tuijianlist:
                        tuijianitem = {}
                        tuijianitem["id"] = info[0]
                        tuijianitem["name"] = info[1]
                        tuijianitem["img"] = info[2]
                        item["tuijian"].append(tuijianitem)
                else:
                    videolist = sess.query(Video.id, Video.name, Video.video_img1).filter(Video.video_img1 != "",
                                                                                          Video.video_img1 != None,
                                                                                          Video.video_src != "",
                                                                                          Video.video_src != None,
                                                                                          Video.id != movieinfo.id).order_by(
                        -Video.id).limit(5).all()
                    for info in videolist:
                        videoitem = {}
                        videoitem["id"] = info[0]
                        videoitem["name"] = info[1]
                        videoitem["img"] = info[2]
                        item["tuijian"].append(videoitem)
                return self.write(
                    json.dumps({"status": 200, "msg": "成功！",'movieinfo':item}, cls=AlchemyEncoder,
                               ensure_ascii=False))
            except:
                print("返回的时候出了问题")
                return self.write(
                    json.dumps({"status": 404, "msg": "找不到页面"}, cls=AlchemyEncoder,
                               ensure_ascii=False))


'''
由于放心不下这个模板毕竟搞了一天半，写的也不怎么好，但是还得继续努力一下，知难而退是好事情，但是迎难而上才是我应该做的。
- 解决思路：
    退步，既然用点击渲染无法做到那就直接使用两种方式结合
../../pages/friend-link/common-link?weburl={weburl}  里面填写web的url地址
../../pages/common/common-video-content?id={id}   视频详情页
../../pages/column/column-info?id={id}   栏目详情页
../../pages/celebrity/celebrity?id={id}  主持人信息页面
'''

affichelinks=[
    {'id':1,'name':"不跳转到任何连接！","linkinfo":"","dataTable":None},
    {'id': 2,'name': "外部网页","linkinfo": "../../pages/friend-link/common-link?weburl=","dataTable":None},
    {'id': 3,'name': "视频详情页","linkinfo": "../../pages/common/common-video-content?id=","dataTable":Micro_video},
    {'id': 4,'name': "栏目详情页","linkinfo": "../../pages/column/column-info?id=","dataTable":Columns},
    {'id': 5,'name': "主持人详情页","linkinfo": "../../pages/celebrity/celebrity?id=","dataTable":Big_V},
    {'id': 6,'name': "电影详情页","linkinfo": "","dataTable":Video},
]

_places = [
            {'typename':'公告','placetype':1,'placelist':
                [
                    {'id':1,'value':'首页的公告','remark':"text_index"},
                    {'id': 2,'value': '电影页的广告','remark':"text_movie"},
                ]
             },
            {'typename': '轮播图','placetype': 2,'placelist':
                [
                    {'id': 3,'value': '首页的轮播图','remark':"img_index"},
                    {'id': 4,'value': '电影页的轮播图','remark':"img_movie"},
                    {'id': 7,'value': '推荐页的轮播图','remark':"img_tuijian"},
                ]
             },
            {'typename': '广告','placetype': 3,'placelist':
                [
                    {'id': 5, 'value': '个人中心的广告', 'remark': "guanggao_gerenzhongxin"},
                    {'id': 6, 'value': '推荐页的广告', 'remark': "guanggao_tuijian"},
                ]
             },
         ]
#添加公告\轮播图\广告图 this 管理
class affiche_manage_page(BaseHandler):
    def get(self, *args, **kwargs):
        places = _places
        # 必须从1开始
        links = affichelinks
        self.render("../templates/000feidemo.html", places=places ,links=links)

#添加数据
class affiche_manage_add(BaseHandler):
    affichelinks = affichelinks
    @auto_rollback
    def post(self, *args, **kwargs):
        print("被请求了！")
        _istype = self.get_argument('_istype')
        _place = self.get_argument('_place')
        _title = self.get_argument('_title')
        _imgsrc = self.get_argument('_imgsrc')
        _linksrc = self.get_argument('_linksrc')
        _linkinfo = self.get_argument('_linkinfo')
        if not [_istype,_place,_title,_imgsrc,_linksrc]:
            print("参数不完整！")
        else:
            types = _istype
            title = _title
            imgsrc = _imgsrc
            place = _place
            linksrc = ""
            for item in affichelinks:
                if int(item['id']) == int(_linksrc):
                    linksrc += str(item["linkinfo"])
                    linksrc += str(_linkinfo)

            try:
                add_data = Affiche(title=title,imgsrc=imgsrc,jumplink=linksrc,place=place,types=types)
                sess.add(add_data)
                sess.commit()
                return self.write(
                json.dumps({"status": 200, "msg": "成功！"}, cls=AlchemyEncoder,
                           ensure_ascii=False))
            except:
                return self.write(
                    json.dumps({"status": 201, "msg": "失败"}, cls=AlchemyEncoder,
                               ensure_ascii=False))

    #获取位置数据
class affiche_manage_getplacedata(BaseHandler):
    affichelinks = affichelinks

    @auto_rollback
    def post(self, *args, **kwargs):
        try:
            place_info = self.get_argument("place_info")
            # 3微视频
            datainfo = []
            for item in affichelinks:
                if int(item["id"]) == int(place_info):
                    data = sess.query(item["dataTable"].id, item["dataTable"].name).order_by(-item["dataTable"].id).all()
                    for value in data:
                        dataitem = {}
                        dataitem["id"] = value[0]
                        dataitem["value"] = value[1]
                        datainfo.append(dataitem)
            # print(datainfo)
            return self.write(
                json.dumps({"status": 200, "msg": "成功",'datainfo':datainfo}, cls=AlchemyEncoder,
                           ensure_ascii=False))
        except:
            return self.write(
                json.dumps({"status": 201, "msg": "失败"}, cls=AlchemyEncoder,
                           ensure_ascii=False))



#验证链接
class affiche_manage_request_link(BaseHandler):
    @auto_rollback
    def post(self, *args, **kwargs):
        url = self.get_argument("url")
        if url:
            url = self.get_argument("url")
            try:
                response = requests.get(url=url)
                if response.status_code == 200:
                    return self.write(
                        json.dumps({"status": 200, "msg": "可用链接"}, cls=AlchemyEncoder,
                                   ensure_ascii=False))
            except:
                return self.write(
                    json.dumps({"status": 200, "msg": "无效链接"}, cls=AlchemyEncoder,
                               ensure_ascii=False))
            else:
                return self.write(
                    json.dumps({"status": 200, "msg": "无效链接"}, cls=AlchemyEncoder,
                               ensure_ascii=False))
        else:
            return self.write(
            json.dumps({"status": 200, "msg": "没有获取到地址"}, cls=AlchemyEncoder,
                       ensure_ascii=False))

#获取所有广告信息

class get_app_common_news_list(BaseHandler):
    @auto_rollback
    def get(self, *args, **kwargs):
        try:
            print("你去了！")
            places = _places
            info_item = {}
            for places_item in places:
                for item in places_item['placelist']:
                    info_item[item["remark"]] = []
                    datalist = sess.query(Affiche).filter(Affiche.place == item['id']).order_by(-Affiche.id).limit(
                        5).all()
                    lenght = len(datalist)
                    for data in datalist:
                        remarkobj = {}
                        remarkobj["text"] = data.title
                        remarkobj["img"] = data.imgsrc
                        remarkobj["tolink"] = data.jumplink
                        remarkobj["lenght"] = lenght
                        info_item[item["remark"]].append(remarkobj)
            return self.write(
                json.dumps({"status":200, "msg": "成功！","info_item":info_item}, cls=AlchemyEncoder,
                           ensure_ascii=False))
        except:
            print("失败!")
            return self.write(
                json.dumps({"status": 500, "msg": "服务器发生错误！"}, cls=AlchemyEncoder,
                           ensure_ascii=False))


class get_app_index_column_list_name(BaseHandler):
    @auto_rollback
    def get(self, *args, **kwargs):
        lanmu = sess.query(Columns).filter(Columns.columns_img != None,Columns.columns_img !="").order_by(-Columns.creation_time).all()
        info_list = []
        for info in lanmu:
            item = {}
            item["id"] = info.id
            item["title"] = info.name
            item["img"] = info.columns_img
            info_list.append(item)
        return self.write(
            json.dumps({"status": 200, "msg": "成功！", "info_list":info_list}, cls=AlchemyEncoder,
                       ensure_ascii=False))
