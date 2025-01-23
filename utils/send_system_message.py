from django.utils import timezone
from users.models import SystemMessage


def send_system_message(recipient, content):
    """发送系统消息"""
    system_message = SystemMessage.objects.create(
        recipient=recipient,
        content=content,
        sent_at=timezone.now()
    )
    return system_message