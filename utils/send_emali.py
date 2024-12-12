"""

from users.models import EmailVerification
from django.core.mail import send_mail
import random
import string

def random_string(length=8):
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    strcode="".join(random.sample(chars,length))
    return strcode

def send_register_email(email,send_type='register'):
    email_verification = EmailVerification()
    code = random_string()
    email_verification.code = code
    email_verification.email = email
    email_verification.send_type = send_type
    email_verification.save()
    if send_type == 'register':
        email_title='博客的注册激活链接'
        email_body='请点击一下链接激活账号：http://127.0.0.1:8000/active/{0}'.format(code)
        send_status=send_mail(email_title,email_body,'yksunnx0828@163.com',[email])
        if send_status:
            pass


"""

