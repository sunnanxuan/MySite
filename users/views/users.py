from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ..models import Follow, User, Message
from django.shortcuts import render, redirect



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
            Message.send_message(sender=request.user, recipient=recipient, content=content)
            return redirect('inbox')  # 跳转到收件箱

    return render(request, 'users/send_message.html', {'recipient': recipient})


@login_required
def inbox_view(request):
    """显示当前用户的收件箱（未读私信）"""
    unread_messages = Message.get_unread_messages(request.user)
    return render(request, 'users/inbox.html', {'unread_messages': unread_messages})


@login_required
def read_message(request, message_id):
    """查看私信并标记为已读"""
    message = get_object_or_404(Message, id=message_id, recipient=request.user)
    message.is_read = True
    message.save()
    return render(request, 'users/read_message.html', {'message': message})




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

    return render(request, 'users/my_followers.html', {
        'follower_users': follower_users,
        'active_menu': 'user-info',
        'active_link': 'my_followers'
    })
