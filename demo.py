#多对多查询分类
import random

from models import *


print()


#####停用
<a style="text-decoration:none" onclick="member_stop(this,'10001')" href="javascript:;" title="停用"><i class="Hui-iconfont"></i></a>
<a style="text-decoration:none"  href="" title="停用"><i class="Hui-iconfont"></i></a>

#####启用
<a onclick="admin_start(this,id)" href="javascript:;" title="启用" style="text-decoration:none"><i class="Hui-iconfont"></i></a>
<a  href="" title="启用" style="text-decoration:none"><i class="Hui-iconfont"></i></a>

#####编辑
<a title="编辑" href="javascript:;" onclick="member_edit('编辑','member-add.html','4','','510')" class="ml-5" style="text-decoration:none"><i class="Hui-iconfont"></i></a>
<a title="编辑" href="" class="ml-5" style="text-decoration:none"><i class="Hui-iconfont"></i></a>

#####修改密码
<a style="text-decoration:none" class="ml-5" onclick="change_password('修改密码','change-password.html','10001','600','270')" href="javascript:;" title="修改密码"><i class="Hui-iconfont"></i></a>
<a style="text-decoration:none" class="ml-5" href="" title="修改密码"><i class="Hui-iconfont"></i></a>

#####删除
<a title="删除" href="javascript:;" onclick="member_del(this,'1')" class="ml-5" style="text-decoration:none"><i class="Hui-iconfont"></i></a>
<a title="删除" href="" class="ml-5" style="text-decoration:none"><i class="Hui-iconfont"></i></a>

#####还原
<a style="text-decoration:none" href="javascript:;" onclick="member_huanyuan(this,'1')" title="还原"><i class="Hui-iconfont"></i></a>
<a style="text-decoration:none" href="" title="还原"><i class="Hui-iconfont"></i></a>

#####审核
<a style="text-decoration:none" onclick="article_shenhe(this,'10001')" href="javascript:;" title="审核"><i class="icon Hui-iconfont"></i></a>
<a style="text-decoration:none"  href="" title="审核"><i class="icon Hui-iconfont"></i></a>

#####下架
<a style="text-decoration:none" onclick="article_stop(this,'10001')" href="javascript:;" title="下架"><i class="Hui-iconfont"></i></a>
<a style="text-decoration:none" href="" title="下架"><i class="Hui-iconfont"></i></a>

#####发布
<a style="text-decoration:none" onclick="article_start(this,id)" href="javascript:;" title="发布"><i class="Hui-iconfont"></i></a>
<a style="text-decoration:none" href="" title="发布"><i class="Hui-iconfont"></i></a>

#####详情
<a title="详情" href="javascript:;" onclick="system_log_show(this,'10001')" class="ml-5" style="text-decoration:none"><i class="Hui-iconfont"></i></a>
<a title="详情" href="" class="ml-5" style="text-decoration:none"><i class="Hui-iconfont"></i></a>

