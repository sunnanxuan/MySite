from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ..models import Follow, User, Message
from django.shortcuts import render, redirect
from django.db.models import Q, F



@login_required
def follow_user(request, user_id):
    # 获取当前用户和目标用户
    current_user = request.user
    author = User.objects.get(id=user_id)

    action = request.GET.get('action')  # 获取动作类型

    if action == 'follow':  # 如果是关注操作
        # 如果当前用户未关注该作者，执行关注
        if not Follow.objects.filter(follower=current_user, followed=author).exists():
            Follow.objects.create(follower=current_user, followed=author)
    elif action == 'unfollow':  # 如果是取消关注操作
        # 如果已经关注，取消关注
        Follow.objects.filter(follower=current_user, followed=author).delete()

    return redirect('blog:author_profile', author_id=author.id)






@login_required
def send_message_view(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)

    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            # 使用 send_message 方法发送消息
            Message.send_message(sender=request.user, recipient=recipient, content=content)
            # 发送后跳转到与该用户的聊天页面
            return redirect('users:chat', user_id=recipient.id)  # 假设 'chat_page' 是聊天页面的 URL 名

    return render(request, 'users/send_message.html', {'recipient': recipient})








@login_required
def message_page(request):
    # 获取当前用户所有消息的发送者和接收者
    received_messages = Message.objects.filter(recipient=request.user).values('sender').distinct()
    sent_messages = Message.objects.filter(sender=request.user).values('recipient').distinct()

    # 获取发送和接收消息的用户
    user_ids = set()
    user_ids.update(received_messages.values_list('sender', flat=True))
    user_ids.update(sent_messages.values_list('recipient', flat=True))

    # 获取所有相关的用户信息
    users = User.objects.filter(id__in=user_ids)

    # 检查每个用户发来的未读消息
    unread_counts = {}
    for user in users:
        # 获取对方发给当前用户的未读消息数量
        unread_count = Message.objects.filter(recipient=request.user, sender=user, is_read=False).count()
        unread_counts[user.id] = unread_count

    print(unread_counts)

    context = {
        'users': users,
        'unread_counts': unread_counts,  # 将未读消息数量传递到模板
        'active_menu': 'message',
        'active_link': 'message'
    }
    return render(request, 'users/message_page.html', context)









@login_required
def chat_page(request, user_id):
    # 获取目标用户
    user = User.objects.get(id=user_id)

    # 获取当前用户与目标用户之间的所有未读消息，并标记为已读
    unread_messages = Message.objects.filter(
        recipient=request.user,  # 收件人是当前用户
        sender=user,             # 发件人是目标用户
        is_read=False            # 仅未读消息
    )

    # 标记为已读
    for message in unread_messages:
        message.mark_as_read()

    # 获取当前用户与目标用户之间的所有消息（包括已读和未读消息）
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=user)) |
        (Q(sender=user) & Q(recipient=request.user))
    ).order_by('sent_at')

    # 渲染模板
    context = {
        'messages': messages,
        'user': user,
        'active_menu': 'message',
        'active_link': 'message'
    }
    return render(request, 'users/chat_page.html', context)




def my_following(request):
    """展示当前用户关注的所有用户"""
    user = request.user

    # 当前用户关注的用户
    following = user.following.values_list('followed', flat=True)
    following_users = User.objects.filter(id__in=following)

    return render(request, 'users/my_following.html', {
        'following_users': following_users,
        'active_menu': 'user-info',
        'active_link': 'my_following'
    })





@login_required
def my_followers(request):
    """展示所有关注当前用户的用户"""
    user = request.user

    # 关注当前用户的用户
    followers = user.followers.values_list('follower', flat=True)
    follower_users = User.objects.filter(id__in=followers)
    following = user.following.values_list('followed', flat=True)
    following_users = User.objects.filter(id__in=following)

    return render(request, 'users/my_followers.html', {
        'follower_users': follower_users,
        'active_menu': 'user-info',
        'active_link': 'my_followers',
        'following_users': following_users,
    })






