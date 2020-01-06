import tornado.web
from views import Index,adminuser,User,AppPort,video,Film,Big_V,Author,Classify,Login,Notice
import config


# 路由
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [


            (r"/phone",Index.Phone),     #手机号验证码   


            (r"/login", Login.Login),                # 管理员登录   
            (r"/register", Login.Register),          # 管理员注册  
            (r"/login_camera", Login.Login_camera),             # 摄制组登录
            (r"/lindex", Login.Lindex),                         # 摄制组首页
            (r"/authordetails", Login.Authordetails),           # 摄制组详情
            (r"/lmicro", Login.Lmicro),                         # 微视频管理
            (r"/lmicro_add", Login.Lmicro_add),                 # 添加微视频信息
            (r'/lmicro_edit/(\d+)', Login.Lmicro_edit),         # 修改微视频
            (r'/lmicro_del/(\d+)', Login.Lmicro_del),           # 删除微视频
            (r'/lmicro_audit/(\d+)', Login.Lmicro_audit),       # 微视频审核
            (r'/lmicro_block/(\d+)', Login.Lmicro_block),       # 微视频下架
            (r'/lmicro_details/(\d+)', Login.Lmicro_details),   # 微视频详情
            (r"/lmicro_picture/(\d+)", Login.Lmicro_picture),   # 微视频图片上传 
            (r'/lmicro_video/(\d+)', Login.Lmicro_video),       # 微视频上传视频



            (r"/product_micro", video.Product_micro),  # 微视频管理
            (r"/product_micro_add", video.Product_micro_add),  # 添加微视频信息
            (r'/product_micro_edit/(\d+)', video.Product_micro_edit),   # 修改微视频
            (r'/product_micro_del/(\d+)', video.Product_micro_del),   # 删除微视频
            (r'/product_micro_audit/(\d+)', video.Product_micro_audit),   # 微视频审核
            (r'/product_micro_block/(\d+)', video.Product_micro_block),   # 微视频下架
            (r'/product_micro_details/(\d+)', video.Product_micro_details),  # 微视频详情
            (r"/product_micro_picture/(\d+)", video.Product_micro_picture),  # 微视频图片上传   
            (r'/product_micro_video/(\d+)', video.Product_micro_video),  # 微视频 上传视频




            (r"/film_list", Film.Film_list),  # 电影管理
            (r"/film_add", Film.Film_add),  # 添加电影
            (r'/film_del/(\d+)', Film.Film_del),   # 修改电影
            (r'/film_edit/(\d+)', Film.Film_edit),   # 删除电影  
            (r'/film_audit/(\d+)', Film.Film_audit),   # 电影审核  
            (r'/film_block/(\d+)', Film.Film_block),   # 电影下架  
            (r'/film_details/(\d+)', Film.Film_details),   # 电影详情
            (r"/film_picture/(\d+)", Film.Film_picture),  # 电影图片上传
            (r'/film_video/(\d+)', Film.Film_video),  # 电影 上传视频

 
            (r"/advertising_list", Notice.Advertising_list),  # 广告管理
            (r"/advertising_add", Notice.Advertising_add),  # 添加广告
            (r'/advertising_del/(\d+)', Notice.Advertising_del),   # 修改广告
            (r'/advertising_edit/(\d+)', Notice.Advertising_edit),   # 删除广告 
            (r'/advertising_audit/(\d+)', Notice.Advertising_audit),   # 广告审核  
            (r'/advertising_block/(\d+)', Notice.Advertising_block),   # 广告下架  
            (r'/advertising_details/(\d+)', Notice.Advertising_details),   # 广告详情
            (r"/advertising_picture/(\d+)", Notice.Advertising_picture),  # 广告图片上传



            (r"/notice_list", Notice.Notice_list),  # 公告管理
            (r"/notice_add", Notice.Notice_add),  # 添加公告
            (r'/notice_del/(\d+)', Notice.Notice_del),   # 修改公告
            (r'/notice_edit/(\d+)', Notice.Notice_edit),   # 删除公告
            (r'/notice_audit/(\d+)', Notice.Notice_audit),   # 公告审核  
            (r'/notice_block/(\d+)', Notice.Notice_block),   # 公告下架  
            (r'/notice_details/(\d+)', Notice.Notice_details),   # 公告详情
            (r"/notice_picture/(\d+)", Notice.Notice_picture),  # 公告图片上传



            (r"/celebrity_list", Big_V.Celebrity_list),  # 明星管理
            (r"/celebrity_add", Big_V.Celebrity_add),  # 添加明星
            (r'/celebrity_del/(\d+)', Big_V.Celebrity_del),   # 删除明星  
            (r'/celebrity_edit/(\d+)', Big_V.Celebrity_edit),   # 修改明星
            (r'/celebrity_details/(\d+)', Big_V.Celebrity_details),   # 明星详情
            (r"/celebrity_picture/(\d+)", Big_V.Celebrity_picture),  # 明星图片上传
            




            (r"/author_list", Author.Author_list),  # 作者管理
            (r"/author_add", Author.Author_add),     # 添加作者
            (r'/author_del/(\d+)', Author.Author_del),   # 删除作者
            (r'/author_edit/(\d+)', Author.Author_edit),   # 修改作者   
            (r'/author_audit/(\d+)', Author.Author_audit),   # 作者审核
            (r'/author_block/(\d+)', Author.Author_block),   # 作者停用
            (r'/author_details/(\d+)', Author.Author_details),   # 作者详情
            (r"/author_picture/(\d+)", Author.Author_picture),  # 作者图片上传




            (r"/user_list",User.User_list),               #用户管理
            (r"/user_add",User.User_add),                    #添加用户
            (r"/user_del/(\d)", User.User_del),            #删除用户   
            (r"/user_audit/(\d)",User.User_audit),          #用户停用   
            (r"/user_start/(\d)", User.User_start),            #用户启用    
            (r"/user_password/(\d)",User.User_password),          #用户修改密码   
            (r"/user_edit/(\d)",User.User_edit),          #修改用户
            (r"/user_details/(\d+)", User.User_details),   # 用户详情
            (r"/user_picture/(\d+)", User.User_picture),  # 用户图片上传
            (r"/user_delete",User.User_delete),       #删除的用户



            (r"/product_category", Classify.Product_category),  # 分类管理
            (r"/product_category_add", Classify.Product_category_add),  # 添加分类
            (r"/product_category_edit/(\d+)", Classify.Product_category_edit),  # 修改分类
            (r"/category_del/(\d+)", Classify.Category_del),  # 删除分类

            (r"/product_column", Classify.Product_column),  # 栏目管理
            (r"/product_column_add", Classify.Product_column_add),  # 添加栏目
            (r"/product_column_picture/(\d+)", Classify.Product_column_picture),  # 栏目封面图上传
            (r"/product_column_edit/(\d+)", Classify.Product_column_edit),  # 修改栏目
            (r"/column_del/(\d+)", Classify.Column_del),  # 删除栏目
              
            (r"/product_label", Classify.Product_label),  # 标签管理
            (r"/product_label_add", Classify.Product_label_add),  # 添加标签 
            (r"/product_label_picture/(\d+)", Classify.Product_label_picture),  # 标签封面图上传
            (r"/product_label_edit/(\d+)", Classify.Product_label_edit),  # 修改标签
            (r"/label_del/(\d+)", Classify.Label_del),  # 删除标签


            (r"/ceshi", AppPort.Ceshi),  # app接口
            (r"/api/uptoken", AppPort.GetToken),
            (r"/demo/uptoken", AppPort.QiNiuHandler),
            (r"/video/micro_list/(\d+)", AppPort.gitVideolist),   #app推荐
            (r"/index/columnsvideolist", AppPort.gitColumnsVideofourList),   #主页-四个视频
            (r"/index/compere_list", AppPort.getIndexCompere_list),  # 主页-首页-主持人-列表
            (r"/index/compere_particulars/(\d+)", AppPort.getIndexCompere_particulars),  # 主页-首页-明星-详情页
            (r"/index/film_videolist", AppPort.getIndexfilm_videolist),  # 主页-电影页-电影列表-详情页
            (r"/common/getverification", AppPort.App_getverification),  # 获取注册验证码
            (r"/app/register_user", AppPort.App_register_user),  # 用户注册
            (r"/app/login_user",AppPort.App_login_user),         #用户登录   

            #############  新增
            (r"/gitVideodetails/(\d+)", AppPort.gitVideodetails),  # 微视频视频详情页    
            (r"/gitColumnsList",AppPort.gitColumnsList),         #栏目列表   
            (r"/gitlabelList",AppPort.gitlabelList),            #标签列表   
            (r"/Send_Data", AppPort.Send_Data),                #手机号验证码   
            (r"/App_login",AppPort.App_login),                 #用户登录   
            (r"/App_register",AppPort.App_register),              #用户登录   









            #主页面操作
            (r"/index", Index.IndexHandler),
            (r"/", Index.Index),  # 首页
            (r"/welcome", Index.Welcome),  # 我的桌面


            #管理员相关 
            (r"/admin_list", adminuser.Admin_list),  # 管理员列表  
            (r"/admin_add", adminuser.Admin_add),  # 管理员添加
            (r"/admin_edit/(\d)", adminuser.Admin_edit),  # 管理员编辑
            (r"/admin_delete/(\d)", adminuser.Admin_delete),  # 管理员编辑

            (r"/feedment_list", Index.Feedment_list),           # 评论列表
            (r"/feedment_del/(\d+)", Index.Feedment_del),       # 删除评论
            (r"/feedback_list", Index.Feedback_list),           # 意见反馈


            (r"/charts_1", Index.Charts_1),  # 折线图
            (r"/charts_2", Index.Charts_2),  # 时间轴折线图
            (r"/charts_3", Index.Charts_3),  # 区域图
            (r"/charts_4", Index.Charts_4),  # 柱状图
            (r"/charts_5", Index.Charts_5),  # 饼状图
            (r"/charts_6", Index.Charts_6),  # 3D柱状图
            (r"/charts_7", Index.Charts_7),  # 3D饼状图


            (r"/system_base", Index.System_base),                    # 系统设置
            (r"/system_shielding", Index.System_shielding),          # 屏蔽词


        ]
        super(Application, self).__init__(handlers, **config.setting)