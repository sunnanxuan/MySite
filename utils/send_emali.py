import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mySite.settings')

import django
django.setup()






from users.models import EmailVerification
import random
import string
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

def random_string(length=8):
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    strcode="".join(random.sample(chars,length))
    return strcode

def send_register_email(email,send_type='register'):
    api_key = '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'  # 替换为您的 SendGrid API 密钥
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
        email_body=Content("text/plain", '请点击一下链接激活账号：http://127.0.0.1:8000/active/{0}'.format(code))


    # 3. 创建邮件对象
        mail = Mail(from_email, to_email, email_title, email_body)

        try:
            response = sg.send(mail)
            print(f"Email sent successfully! Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")











"""

import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

# 1. 设置 SendGrid API 密钥
api_key = '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'  # 替换为您的 SendGrid API 密钥
sg = sendgrid.SendGridAPIClient(api_key=api_key)

# 2. 创建邮件内容
from_email = Email("yksunnx0828@163.com")  # 替换为发送邮件的邮箱地址
to_email = To("nanxuan.sun@gmail.com")  # 替换为收件人邮箱地址
subject = "试试谷歌邮箱好不好使"
content = Content("text/plain", "我再试试能不能发过去")

# 3. 创建邮件对象
mail = Mail(from_email, to_email, subject, content)

# 4. 发送邮件
try:
    response = sg.send(mail)
    print(f"Email sent successfully! Status code: {response.status_code}")
    print(f"Response body: {response.body}")
    print(f"Response headers: {response.headers}")
except Exception as e:
    print(f"An error occurred: {e}")


"""
