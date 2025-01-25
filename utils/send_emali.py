import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mySite.settings')

import django
django.setup()






from users.models import EmailVerification
import random
import string
import sendgrid
from django.conf import settings
from sendgrid.helpers.mail import Mail, Email, To, Content

def random_string(length=8):
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    strcode="".join(random.sample(chars,length))
    return strcode

def send_register_email(email,send_type='register'):
    api_key = settings.SENDGRID_API_KEY
    sg = sendgrid.SendGridAPIClient(api_key=api_key)

    # 2. 创建邮件内容
    email_verification = EmailVerification()
    code = random_string()
    email_verification.code = code
    email_verification.email = email
    email_verification.send_type = send_type
    email_verification.save()

    from_email = Email("yksunnx0828@163.com")  # 替换为发送邮件的邮箱地址
    to_email = To(email)  # 替换为收件人邮箱地址

    if send_type == 'register':
        email_title='博客的注册激活链接'
        email_body=Content("text/plain", '请点击一下链接激活账号：http://127.0.0.1:8000/users/active/{0}'.format(code))
        mail = Mail(from_email, to_email, email_title, email_body)

        try:
            response = sg.send(mail)
            print(f"Email sent successfully! Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")

    else:
        email_title = '找回密码'
        email_body = Content("text/plain", '请点击一下链接修改密码：http://127.0.0.1:8000/users/forget_pwd_url/{0}'.format(code))
        mail = Mail(from_email, to_email, email_title, email_body)

        try:
            response = sg.send(mail)
            print(f"Email sent successfully! Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")













