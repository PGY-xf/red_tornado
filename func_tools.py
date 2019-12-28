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



