
from django.conf import  settings
from django.core.mail import send_mail
from celery import Celery
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Crm.settings')
django.setup()
import time

# 创建一个Celery类的实例对象
app = Celery('celery_tasks.email_tasks',broker='redis://192.168.13.167:6379/8')

@app.task
def send_register_active_email(to_email, username, token):
    '''发送激活邮件'''
    # 组织邮件信息
    subject = '天天生鲜欢迎信息'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = '<h1>%s, 欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的账户<br/><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (username, token, token)
    # 因为是里面含有标签的信息, 所以放到html_message
    send_mail(subject, message, sender, receiver, html_message=html_message)
    time.sleep(5)

# from django.template import loader
# @app.task
# # 用户没有登录页面才是完全一样的
# def genertate_static_index_html():
#      # 首页的所有页面数据
#     save = os.path.join()
#     loader.get_template('static_index')