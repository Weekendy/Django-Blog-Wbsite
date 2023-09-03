from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import UserProperty
from .forms import *
from blogs.views import blogpost_list
from tools import judge_pc_or_mobile

# 非视图功能性方法：在关注发生变化时手动调用，改变两个用户关注的数量
def change_follownum(user1_id, user2_id):
    # user1为关注者， user2为被关注者
    user1_p = User.objects.get(id=user1_id).property
    user2_p = User.objects.get(id=user2_id).property
    follow_num = len(user1_p.follow.all())
    followed_num = len(user2_p.followed.all())
    user1_p.follow_num = follow_num
    user2_p.followed_num = followed_num
    user1_p.save()
    user2_p.save()

# 注册
def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            user_property = UserProperty(user=new_user)
            user_property.save()
            login(request, new_user)
            return redirect('blogs:index')

    context = {'form' : form}
    return render(request, 'registration/register.html', context)

# 用户查看界面
def user(request, user_id):
    see_user = User.objects.get(id=user_id)
    if not see_user.is_active:
        return HttpResponse("这个账号不存在或已被注销")

    if request.user.is_authenticated:
        request.user.property.perweb = request.path
        request.user.property.save()

    user_p = see_user.property

    # 设置用户列表中的用户是否被关注
    if request.user.is_authenticated:
        user_p.is_followed = user_p.id in [followed_user_p.id for followed_user_p in request.user.property.follow.all()]
    else:
        user_p.is_followed = True

    ua = request.META.get("HTTP_USER_AGENT")
    is_pc = not judge_pc_or_mobile(ua)
    context = {
        'see_user': see_user,
        'user_p': user_p,
        'is_pc': is_pc
        }
    return render(request, 'users/user.html', context)



# 关注
@login_required
def follow(request, user2_id):
    if request.user.id == user2_id:
        return redirect('users:user', user2_id)
    if not User.objects.get(id=user2_id).is_active:
        return HttpResponse("这个账号不存在或已被注销")

    # user1为关注者， user2为被关注者
    user1_p = User.objects.get(id=request.user.id).property
    user2_p = User.objects.get(id=user2_id).property
    user1_p.follow.add(user2_p.id)
    user1_p.follow_num = len(user1_p.follow.all())
    user1_p.followed_num = len(user1_p.followed.all())
    user2_p.follow_num = len(user2_p.follow.all())
    user2_p.followed_num = len(user2_p.followed.all())
    user1_p.save()
    user2_p.save()

    print(user2_p.user)
    print(user2_p.user.id)
    print(user2_p)
    print(user2_p.id)

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def defollow(request, user2_id):
    if request.user.id == user2_id:
        return redirect('users:user', user2_id)
    if not User.objects.get(id=user2_id).is_active:
        return HttpResponse("这个账号不存在或已被注销")

    # user1为关注者， user2为被关注者
    user1_p = User.objects.get(id=request.user.id).property
    user2_p = User.objects.get(id=user2_id).property
    user1_p.follow.remove(user2_p.id)
    user1_p.follow_num = len(user1_p.follow.all())
    user1_p.followed_num = len(user1_p.followed.all())
    user2_p.follow_num = len(user2_p.follow.all())
    user2_p.followed_num = len(user2_p.followed.all())
    user1_p.save()
    user2_p.save()

    print(user2_p.user)
    print(user2_p.user.id)
    print(user2_p)
    print(user2_p.id)

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def follow_list(request, user_id):
    if request.user.is_authenticated:
        request.user.property.perweb = request.path
        request.user.property.save()

    see_user = User.objects.get(id=user_id)
    if not see_user.is_active:
        return HttpResponse("这个账号不存在或已被注销")

    # 设置用户列表中的用户是否被关注
    followed_users_p = User.objects.get(id=user_id).property.follow.all()
    for user_p in followed_users_p:
        user_p.is_followed = user_p.id in [followed_user_p.id for followed_user_p in request.user.property.follow.all()]

    context = {'see_user': see_user, 'users_p': followed_users_p}
    return render(request, 'users/user_list.html', context)

# 粉丝列表
def followed_list(request, user_id):
    if request.user.is_authenticated:
        request.user.property.perweb = request.path
        request.user.property.save()

    see_user = User.objects.get(id=user_id)
    if not see_user.is_active:
        return HttpResponse("这个账号不存在或已被注销")

    # 设置用户列表中的用户是否被关注
    follow_users_p = User.objects.get(id=user_id).property.followed.all()
    for user_p in follow_users_p:
        user_p.is_followed = user_p.id in [followed_user_p.id for followed_user_p in request.user.property.follow.all()]

    context = {'see_user': see_user, 'users_p': follow_users_p}
    return render(request, 'users/user_list.html', context)



# 用户发表的帖子列表
def mypost_list(request, user_id):
    if not (User.objects.get(id=user_id).is_active):
        raise Http404

    if request.user.is_authenticated:
        request.user.property.perweb = request.path
        request.user.property.save()

    posts = User.objects.get(id=user_id).blogpost_set.filter(activate=True).order_by('-date_added')
    for post in posts:
        post.is_my = True
    return blogpost_list(request, posts)

# 用户喜欢的帖子列表
def likepost_list(request, user_id):
    if not (User.objects.get(id=user_id).is_active):
        raise Http404

    if request.user.is_authenticated:
        request.user.property.perweb = request.path
        request.user.property.save()

    posts = []
    for like in User.objects.get(id=user_id).like.order_by('-date_added'):
        like.blogpost.time = like.date_added
        posts.append(like.blogpost)
    return blogpost_list(request, posts)

# 用户浏览记录列表
def logpost_list(request, user_id):
    user = User.objects.get(id=user_id)
    if not (user.is_active) or request.user.id != user_id:
        raise Http404

    if request.user.is_authenticated:
        request.user.property.perweb = request.path
        request.user.property.save()

    posts = []
    for log in User.objects.get(id=user_id).property.blogwatchlog_set.order_by('-date_added'):
        log.blogpost.log_time = log.date_added
        log.blogpost.is_log = True
        posts.append(log.blogpost)
            
    return blogpost_list(request, posts)

@login_required
def edit_property(request):
    user = User.objects.get(id=request.user.id)
    user_p = request.user.property

    user_p.perweb = request.path
    user_p.save()

    if request.method != 'POST':
        form = UserPropertyForm(instance=user_p)
    else:
        form = UserPropertyForm(instance=user_p, data=request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            if form.cleaned_data['username'] != '':
                p.user.username = form.cleaned_data['username']
            p.user.save()
            p.save()
            return redirect('users:edit_property')

    context = {'form': form, 'birthday': user_p.birthday}
    return render(request, 'users/edit_property.html', context)