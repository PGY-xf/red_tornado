import time

# #获取昨天日期
# import datetime
# # def getYesterday(): 
# #     today=datetime.date.today() 
# #     oneday=datetime.timedelta(days=1) 
# #     yesterday=today-oneday  
# #     return yesterday
 
# # # 输出
# # print(getYesterday())


# today = datetime.date.today()
# # 开始日期
# abc = today - datetime.timedelta(days=today.weekday()+7)
# # 结束日期
# abd = today - datetime.timedelta(days=today.weekday()+1)
# print(today,abc,abd)


# # 获取当前日期 
# date = datetime.datetime.now()
# # 上周开始时间
# date1 = date-datetime.timedelta(days=date.weekday()+7)
# # 上周结束时间
# date2 = date-datetime.timedelta(days=date.weekday()+1)
# print(date,date1,date2)
# #0 tm_year	  年(4位数)  2008
# #1 tm_mon	  月	       1 到 12
# #2 tm_mday	  日	       1到31
# #3 tm_hour	  小时	   0到23
# #4 tm_min	  分钟	   0到59
# #5 tm_sec	  秒	       0到61 (60或61 是闰秒)
# #6 tm_wday    一周的第几日	0到6 (0是周一)
# #7 tm_yday	  一年的第几日	1到366 (儒略历)
# #8 tm_isdst	  夏令时	        -1, 0, 1, -1是决定是否为夏令时的旗帜

# # localtime = time.localtime(time.time())
# # print("本地时间:", localtime)
# # tm_year = localtime.tm_year    #年
# # tm_mon = localtime.tm_mon      #月
# # tm_mday = localtime.tm_mday    #日
# # tm_hour = localtime.tm_hour    #小时
# # tm_min = localtime.tm_min      #分钟
# # tm_sec = localtime.tm_sec      #秒
# # tm_wday = localtime.tm_wday    #一周的第几日
# # tm_yday = localtime.tm_yday    #一年的第几日

# times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# print("当前时间:", times)

# # localtime = time.asctime( time.localtime(time.time()) )
# # print("本地时间:", localtime)

# # localtime = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()) 
# # print(localtime)

# # a = "Sat Mar 28 22:24:24 2016"
# # localtime = time.mktime(time.strptime(a,"%a %b %d %H:%M:%S %Y"))
# # print(localtime)


# import datetime
# from datetime import timedelta
  
# now = datetime.datetime.now()

# #今天
# today = now
# print(today)
# #昨天
# yesterday = now - timedelta(days=1)
# print(yesterday) 
# #明天
# tomorrow = now + timedelta(days=1) #当前季度
# now_quarter = now.month / 3 if now.month % 3 == 0 else now.month / 3 + 1
# print(tomorrow,now_quarter)
# #本周第一天和最后一天
# this_week_start = now - timedelta(days=now.weekday())
# this_week_end = now + timedelta(days=6-now.weekday())
# print(this_week_start,this_week_end)
# #上周第一天和最后一天
# last_week_start = now - timedelta(days=now.weekday()+7)
# last_week_end = now - timedelta(days=now.weekday()+1)
# print(last_week_start,last_week_end)
  




# import time
# import datetime
# # 获取当前日期 
# date = datetime.datetime.now()
# year = date.year
# month = date.month
# # 开始日期
# start = datetime.date(year, month, 1)
# #结束日期
# if month == 12:
#     end = datetime.date(year+1, 1, 1) - datetime.timedelta(days=1)
# else:
#     end = datetime.date(year, month+1, 1) - datetime.timedelta(days=1)

# print(start,month)


# import datetime


# today = datetime.date.today()
# today.day
# # 今天（日期）
# a = today.isoformat()                # out: '2019-02-22'
# print("今天日期:",a)
# #  昨天
# today = datetime.date.today()
# yesterday = today + datetime.timedelta(days=-1)
# b = yesterday.isoformat()                                   # out: '2019-02-21'
# print("昨天日期:",b)
 
# # 明天
# today = datetime.date.today()
# yesterday = today + datetime.timedelta(days=1)
# c = yesterday.isoformat()                                   # out: '2019-02-23'
# print("明天日期:",c)
 
# # 本周第一天
# today = datetime.date.today()
# week_start_day = today - datetime.timedelta(days=today.weekday())
# d = week_start_day.isoformat()   # '2019-02-18'，周一
# print("本周第一天:",d)

# # 本周最后一天
# today = datetime.date.today()
# week_end_day = today + datetime.timedelta(days=6-today.weekday())
# e = week_end_day.isoformat()                                   # '2019-02-24'，周天
# print("本周最后一天:",e)

# # 本月第一天
# today = datetime.date.today()
# month_start_day = today - datetime.timedelta(days=today.day-1)
# f = month_start_day.isoformat()                                   # '2019-02-01'，当月第一天
# print("本月第一天:",f)
# # 本月最后一天
# from dateutil.relativedelta import relativedelta            # 引入新的包
# today = datetime.date.today()
# # 必须先置为首日，直接用relativedelta(months=1,days=-today.day+1)会有错误结果
# month_end_day = (today + datetime.timedelta(days=-today.day+1)) + relativedelta(months=1,days=-1)
# g = month_end_day.isoformat()  
# print("本月最后一天:",g)


# # 本周第一天
# today = datetime.date.today()
# week_start_day = today - datetime.timedelta(days=today.weekday())
# d = week_start_day.isoformat()   # '2019-02-18'，周一
# print("本周第一天:",d)

# # 本周第二天
# today = datetime.date.today()
# week_start_day = today - datetime.timedelta(days=today.weekday())
# d = week_start_day.isoformat()   # '2019-02-18'，周一
# print("本周第二天:",d)


# # 本周第三天
# today = datetime.date.today()
# week_start_day = today - datetime.timedelta(days=today.weekday())
# d = week_start_day.isoformat()   # '2019-02-18'，周一
# print("本周第三天:",d)

# # 本周第四天
# today = datetime.date.today()
# week_end_day = today + datetime.timedelta(days=3-today.weekday())
# e = week_end_day.isoformat()                                   # '2019-02-24'，周天
# print("本周第四天:",e)

# # 本周第五天
# today = datetime.date.today()
# week_end_day = today + datetime.timedelta(days=4-today.weekday())
# e = week_end_day.isoformat()                                   # '2019-02-24'，周天
# print("本周第五天:",e)

# # 本周第六天
# today = datetime.date.today()
# week_end_day = today + datetime.timedelta(days=5-today.weekday())
# e = week_end_day.isoformat()                                   # '2019-02-24'，周天
# print("本周第六天:",e)

# # 本周最后一天
# today = datetime.date.today()
# week_end_day = today + datetime.timedelta(days=6-today.weekday())
# e = week_end_day.isoformat()                                   # '2019-02-24'，周天
# print("本周最后一天:",e)

 

import datetime
from datetime import timedelta
now = datetime.datetime.now()
#本周日期
today = now
# this_week_end1 = (now - datetime.timedelta(days=now.weekday())).strftime('%Y-%m-%d')
# this_week_end2 = (now + datetime.timedelta(days=1-now.weekday())).strftime('%Y-%m-%d')
# this_week_end3 = (now + datetime.timedelta(days=2-now.weekday())).strftime('%Y-%m-%d')
# this_week_end4 = (now + datetime.timedelta(days=3-now.weekday())).strftime('%Y-%m-%d')
# this_week_end5 = (now + datetime.timedelta(days=4-now.weekday())).strftime('%Y-%m-%d')
# this_week_end6 = (now + datetime.timedelta(days=5-now.weekday())).strftime('%Y-%m-%d')
# this_week_end7 = (now + datetime.timedelta(days=6-now.weekday())).strftime('%Y-%m-%d')
# print(this_week_end1)
# print(this_week_end2)
# print(this_week_end3)
# print(this_week_end4)
# print(this_week_end5)
# print(this_week_end6)
# print(this_week_end7)



# today = now
# this1 = (now - datetime.timedelta(days=now.weekday())).strftime('%Y-%m-%d')
# this2 = (now + datetime.timedelta(days=1-now.weekday())).strftime('%Y-%m-%d')
# this3 = (now + datetime.timedelta(days=2-now.weekday())).strftime('%Y-%m-%d')
# this4 = (now + datetime.timedelta(days=3-now.weekday())).strftime('%Y-%m-%d')
# this5 = (now + datetime.timedelta(days=4-now.weekday())).strftime('%Y-%m-%d')
# this6 = (now + datetime.timedelta(days=5-now.weekday())).strftime('%Y-%m-%d')
# this7 = (now + datetime.timedelta(days=6-now.weekday())).strftime('%Y-%m-%d')
# abc = this1,this2,this3,this4,this5,this6
# print(abc)
