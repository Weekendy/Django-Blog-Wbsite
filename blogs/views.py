import os
import re
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from blog import settings
from .models import BlogPost, Tag, LikeBlogPost
from users.models import BlogWatchLog
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404
from tools import judge_pc_or_mobile, judge_activate

TAG_MESSAGEE = '此标签已被屏蔽或删除'
POST_MESSAGE = '此贴子已被屏蔽或删除'
COMMENT_MESSAGE = '此评论已被屏蔽或删除'

# 非视图功能性方法：在评论类发生变化时手动调用，改变单个帖子的评论数量
def change_commentnum(post_id):
    blogpost = BlogPost.objects.filter(activate=True).get(id=post_id)
    comment_num = len(blogpost.blogpostcomment_set.filter(activate=True).all())
    for blogpost_comment in blogpost.blogpostcomment_set.filter(activate=True).all():
        comment_num += len(blogpost_comment.intercomment_set.filter(activate=True).all())
    blogpost.comment_num = comment_num
    blogpost.save()

# 非视图功能性方法：在博客媒体发生变化时手动调用，改变单个帖子的图片数量
def change_imagenum(post_id):
    blogpost = BlogPost.objects.filter(activate=True).get(id=post_id)
    image_num = len(blogpost.blogpostmedia_set.filter(activate=True).all())
    blogpost.image_num = image_num
    blogpost.save()

# 非视图模板性方法：传入复数个帖子参数，再以blogpost_list.html渲染
def blogpost_list(request, posts):
    for post in posts:    
        post.tagsO = post.tags.all()
    context = {'posts': posts}
    return render(request, 'blogs/blogpost_list.html', context)

    

# 首页
def index(request):
    if request.user.is_authenticated:
        request.user.property.perweb = request.path
        request.user.property.save()

    return render(request, 'blogs/index.html')



#新建标签
@login_required
def new_tag(request):
    if request.user.is_authenticated:
        request.user.property.perweb = request.path
        request.user.property.save()

    if request.method != 'POST':
        form = TagForm()
    else:
        form = TagForm(data=request.POST)
        # 若表单合法且没有相同文本的标签，则新建标签
        if form.is_valid() and len(Tag.objects.filter(text=form.cleaned_data['text'])) == 0:
            newtag = form.save(commit=False)
            newtag.owner = User.objects.get(id=request.user.id)
            newtag.save()
            return redirect('blogs:tags')
    context = {'form': form}
    return render(request, 'blogs/new_tag.html', context)

# 标签一览
def tags(request):
    if request.user.is_authenticated:
        request.user.property.perweb = request.path
        request.user.property.save()

    tags = Tag.objects.filter(activate=True).order_by('date_added')
    max_post_num = max([len(tag.blogposts.filter(activate=True)) for tag in tags])# 顶尖句子，取帖子数量最大的标签的帖子数量
    for tag in tags:
        tag.size = 24 * (len(tag.blogposts.filter(activate=True)) / max_post_num) + 16
        tag.opacity = 35 * (len(tag.blogposts.filter(activate=True)) / max_post_num) + 65
    context = {'tags': tags}
    return render(request, 'blogs/tags.html', context)

# 单个标签
def tag(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    judge_activate(tag, TAG_MESSAGEE)

    if request.user.is_authenticated:
        request.user.property.perweb = request.path
        request.user.property.save()

    ua = request.META.get("HTTP_USER_AGENT")
    is_pc = not judge_pc_or_mobile(ua)
    posts = tag.blogposts.all().order_by('-date_added')
    for post in posts:
        if not post.is_top:
            if len(post.title) > 20:
                post.title = post.title[:20] + '...'
            if len(post.text) > 60:
                post.text = post.text[:120] + '...'
    
        post.tagsO = post.tags.all()
        if is_pc:
            post.medias = post.blogpostmedia_set.filter(activate=True).order_by('date_added')[:3]
        else:
            post.media = post.blogpostmedia_set.filter(activate=True).order_by('date_added').first()
    
    context = {'posts' : posts, 'is_pc': is_pc}
    return render(request, 'blogs/blogposts.html', context)

# 为帖子增加标签
@login_required
def add_tag(request, post_id):
    post = BlogPost.objects.get(id=post_id)
    judge_activate(post, POST_MESSAGE)
    
    if post.owner.id != request.user.id:
        raise Http404

    if request.method != 'POST':
        form = TagForm()
    else:
        form = TagForm(data=request.POST)
        if form.is_valid():
            added_tag = form.cleaned_data['text']
            # 如果标签未存在，则新建标签且与帖子绑定 若存在，则直接绑定
            tag = Tag.objects.get_or_create(text=added_tag, owner=User.objects.get(id=request.user.id))
            judge_activate(tag, TAG_MESSAGEE)
            tag.save()
            post.tags.add(tag)
            post.save()
            return redirect('blogs:add_tag', post_id)

    tags = post.tags.filter(activate=True).order_by('-date_added')
    context = {'form': form, 'post': post, 'tags': tags}
    return render(request, 'blogs/add_tag.html', context)

# 为帖子解绑标签
@login_required
def unbind_tag(request, post_id, tag_id):
    blogpost = BlogPost.objects.get(id=post_id)
    judge_activate(blogpost, POST_MESSAGE)
    if blogpost.owner.id != request.user.id:
        raise Http404

    blogpost.tags.remove(tag_id)
    return redirect('blogs:add_tag', post_id)
    


# 新建帖子
@login_required
def new_blogpost(request):
    request.user.property.perweb = request.path
    request.user.property.save()

    #若不是POST就准备新表单，是POST就准备数据并新建数据
    if request.method != 'POST':
        form = BlogPostForm()
    else:
        form = BlogPostForm(data=request.POST)
        if form.is_valid():
            new_blogpost = form.save(commit=False)
            new_blogpost.owner = User.objects.get(id=request.user.id)
            new_blogpost.save()
            return redirect('blogs:add_photo', new_blogpost.id)
    context = {'form': form}
    return render(request, 'blogs/new_blogpost.html', context)

# 全帖一览
def blogposts(request):
    if request.user.is_authenticated:
        request.user.property.perweb = request.path
        request.user.property.save()

    ua = request.META.get("HTTP_USER_AGENT")
    is_pc = not judge_pc_or_mobile(ua)
    posts = BlogPost.objects.filter(activate=True).order_by('-date_added')
    for post in posts:
        if not post.is_top:
            if len(post.title) > 20:
                post.title = post.title[:20] + '...'
            if len(post.text) > 60:
                post.text = post.text[:120] + '...'
    
        post.tagsO = post.tags.all()
        if is_pc:
            post.medias = post.blogpostmedia_set.filter(activate=True).order_by('date_added')[:3]
        else:
            post.media = post.blogpostmedia_set.filter(activate=True).order_by('date_added').first()
    
    context = {'posts' : posts, 'is_pc': is_pc}
    return render(request, 'blogs/blogposts.html', context)

# 单个博客帖子
def blogpost(request, post_id):
    post = BlogPost.objects.get(id=post_id)
    judge_activate(post, POST_MESSAGE)

    
    is_return = bool(re.search(request.path, request.META['HTTP_REFERER']))
    if request.user.is_authenticated and (not is_return):
        user_p = request.user.property
        user_p.perweb = request.path
        user_p.save()
        blog_watch_log = BlogWatchLog(user_property=user_p, blogpost=post)
        blog_watch_log.save()
        # 以一种很合理的方法控制浏览记录在200内
        if len(user_p.blogwatchlog_set.all()) > 200:
            user_p.blogwatchlog_set.order_by('date_added').first().delete()
    
    # 准备并传输需要的数据：帖子，表单，评论等
    tags = post.tags.filter(activate=True).order_by('-date_added')
    blogpostcomment_form = BlogPostCommentForm()
    intercomment_form = InterCommentForm()
    comments = post.blogpostcomment_set.filter(activate=True).order_by('date_added')
    inter_commentss = []
    post.is_like = False
    for comment in comments:
        # 使用暴力手段设置评论是否已被用户点赞
        if request.user in comment.like_user.all():
            comment.is_like = True
        else:
            comment.is_like = False
        # 获取楼中楼评论
        inter_commentss.append(comment.intercomment_set.filter(activate=True).order_by('date_added'))
    
    for inter_comments in inter_commentss:
        for inter_comment in inter_comments:
            # 设置楼中楼评论用户是否点赞
            if request.user in inter_comment.like_user.all():
                inter_comment.is_like = True
            else:
                inter_comment.is_like = False
            # 若是回复楼中楼的评论则加上“回复”字段
            if inter_comment.reflected_comment:
                inter_comment.text = "回复 " + inter_comment.reflected_comment.owner.username + '：' + inter_comment.text
            
    # 设置帖子用户是否点赞
    if request.user in [like.user for like in post.like.all()]:
        post.is_like = True
    medias = post.blogpostmedia_set.filter(activate=True).order_by('date_added')
    context = {
        'post': post,
        'tags': tags,
        'comments': comments,
        'inter_commentss': inter_commentss,
        'blogpostcomment_form': blogpostcomment_form,
        'intercomment_form': intercomment_form,
        'medias': medias,
    }
    return render(request, 'blogs/blogpost.html', context)

# 编辑帖子
@login_required
def edit_blogpost(request, post_id):
    post = BlogPost.objects.get(id=post_id)
    judge_activate(post, POST_MESSAGE)
    if post.owner.id != request.user.id:
        raise Http404

    request.user.property.perweb = request.path
    request.user.property.save()

    if request.method != 'POST':
        form = BlogPostForm(instance=post)
    else:
        form = BlogPostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:blogpost', post_id)

    context = {'form': form, 'post': post}
    return render(request, 'blogs/edit_blogpost.html', context)

# 喜欢帖子
@login_required
def like_blogpost(request, post_id):
    blogpost = BlogPost.objects.get(id=post_id)
    judge_activate(blogpost, POST_MESSAGE)

    if len(LikeBlogPost.objects.filter(user=User.objects.get(id=request.user.id), blogpost=blogpost)) < 1:
        like = LikeBlogPost(user=User.objects.get(id=request.user.id), blogpost=blogpost)
        like.save()
    blogpost.like_num = len(blogpost.like.all())
    blogpost.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

# 取消喜欢帖子
@login_required
def delike_blogpost(request, post_id):
    blogpost = BlogPost.objects.get(id=post_id)
    judge_activate(blogpost, POST_MESSAGE)

    LikeBlogPost.objects.get(user=User.objects.get(id=request.user.id), blogpost=blogpost).delete()
    blogpost.like_num = len(blogpost.like.all())
    blogpost.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

# 删除帖子
@login_required
def del_blogpost(request, post_id):
    blogpost = BlogPost.objects.get(id=post_id)
    judge_activate(blogpost, POST_MESSAGE)
    if blogpost.owner.id != request.user.id:
        raise Http404

    blogpost.activate = False
    blogpost.save()
    return redirect('users:mypost_list')



# 为帖子上传图片
@login_required
def add_photo(request, post_id):
    post = BlogPost.objects.get(id=post_id)
    judge_activate(post, POST_MESSAGE)
    if post.owner.id != request.user.id:
        raise Http404

    medias = post.blogpostmedia_set.order_by('date_added')
    if len(request.user.blogpostmedia_set.all()) > 12 and (not request.user.is_staff):
        return redirect('blogs:add_tag', post_id)

    if request.method != 'POST':
        form = BlogPostMediaform()
    else:
        form = BlogPostMediaform(files=request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.owner = User.objects.get(id=request.user.id)
            photo.blogpost = post
            photo.save()
            change_imagenum(post_id)
            return redirect('blogs:add_photo', post_id)
    
    context = {'form': form, 'post': post, 'medias': medias}
    return render(request, 'blogs/add_photo.html', context)

# 删除博客帖子图片
@login_required
def del_photo(request, media_id):
    media = BlogPostMedia.objects.get(id=media_id)
    judge_activate(media.blogpost, POST_MESSAGE)
    if media.owner.id != request.user.id:
        raise Http404
    
    post_id = media.blogpost.id
    os.remove(os.path.join(settings.MEDIA_ROOT, str(media.image)))
    media.delete()
    change_imagenum(post_id)
    return redirect('blogs:add_photo', post_id)
 


# 新建博客帖子评论
@login_required
def new_blogpostcomment(request, post_id):
    post = BlogPost.objects.get(id=post_id)
    judge_activate(post, POST_MESSAGE)

    if request.method != 'POST':
        form = BlogPostCommentForm()
    else:
        form = BlogPostCommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.owner = User.objects.get(id=request.user.id)
            new_comment.blogpost = post
            new_comment.floor_num = new_comment.blogpost.blogpostcomment_set.all().__len__()
            change_commentnum(post_id)
            new_comment.save()
            change_commentnum(new_comment.blogpost.id)
            return redirect('blogs:blogpost', post_id)
    context = {'form': form}
    return render(request, 'blogs/blogpost.html', context)

# 喜欢博客帖子评论
@login_required
def like_blogpostcomment(request, blogpost_comment_id):
    blogpost_comment = BlogPostComment.objects.get(id=blogpost_comment_id)
    judge_activate(blogpost_comment.blogpost, POST_MESSAGE)
    judge_activate(blogpost_comment, COMMENT_MESSAGE)

    post_id = blogpost_comment.blogpost.id
    blogpost_comment.like_user.add(request.user.id)
    blogpost_comment.like_num = len(blogpost_comment.like_user.all())
    blogpost_comment.save()
    return redirect('blogs:blogpost', post_id)

# 取消喜欢博客帖子评论
@login_required
def delike_blogpostcomment(request, blogpost_comment_id):
    blogpost_comment = BlogPostComment.objects.get(id=blogpost_comment_id)
    judge_activate(blogpost_comment.blogpost, POST_MESSAGE)
    judge_activate(blogpost_comment, COMMENT_MESSAGE)
    
    post_id = blogpost_comment.blogpost.id
    blogpost_comment.like_user.remove(request.user.id)
    blogpost_comment.like_num = len(blogpost_comment.like_user.all())
    blogpost_comment.save()
    return redirect('blogs:blogpost', post_id)

# 删除博客帖子评论
@login_required
def del_blogpostcomment(request, blogpost_comment_id):
    blogpost_comment = BlogPostComment.objects.get(id=blogpost_comment_id)
    judge_activate(blogpost_comment.blogpost, POST_MESSAGE)
    judge_activate(blogpost_comment, COMMENT_MESSAGE)
    if blogpost_comment.owner.id != request.user.id:
        raise Http404

    post_id = blogpost_comment.blogpost.id
    blogpost_comment.activate = False
    blogpost_comment.save()
    change_commentnum(post_id)
    return redirect('blogs:blogpost', post_id)



# 新建楼中楼评论（回复外部评论）
@login_required
def new_intercomment(request, extercomment_id):
    extercomment = BlogPostComment.objects.get(id=extercomment_id)
    judge_activate(extercomment.blogpost, POST_MESSAGE)
    judge_activate(extercomment, COMMENT_MESSAGE)

    if request.method == 'POST' and request.POST['text']:
        form = InterCommentForm(data=request.POST)
        new_comment = form.save(commit=False)
        new_comment.owner = User.objects.get(id=request.user.id)
        new_comment.exter_comment = extercomment
        change_commentnum(new_comment.exter_comment.blogpost.id)
        new_comment.save()
        change_commentnum(new_comment.exter_comment.blogpost.id)
        return redirect('blogs:blogpost', new_comment.exter_comment.blogpost.id)
    return redirect('blogs:blogposts')

# 新建楼中楼评论（回复楼中楼评论）
@login_required
def new_intercomment2(request, intercomment_id):
    intercomment = InterComment.objects.get(id=intercomment_id)
    judge_activate(intercomment.extercomment.blogpost, POST_MESSAGE)
    judge_activate(intercomment, COMMENT_MESSAGE)

    if request.method == 'POST' and request.POST['text']:
        form = InterCommentForm(data=request.POST)
        new_comment = form.save(commit=False)
        new_comment.owner = User.objects.get(id=request.user.id)
        new_comment.reflected_comment = InterComment.objects.get(id=intercomment_id)
        new_comment.exter_comment = new_comment.reflected_comment.exter_comment
        change_commentnum(new_comment.exter_comment.blogpost.id)
        new_comment.save()
        change_commentnum(new_comment.exter_comment.blogpost.id)
        return redirect('blogs:blogpost', new_comment.exter_comment.blogpost.id)
    return redirect('blogs:blogposts')

# 喜欢楼中楼评论
@login_required
def like_intercomment(request, intercomment_id):
    intercomment = InterComment.objects.get(id=intercomment_id)
    judge_activate(intercomment.extercomment.blogpost, POST_MESSAGE)
    judge_activate(intercomment, COMMENT_MESSAGE)

    post_id = intercomment.exter_comment.blogpost.id
    intercomment.like_user.add(request.user.id)
    intercomment.like_num = len(intercomment.like_user.all())
    intercomment.save()
    return redirect('blogs:blogpost', post_id)

# 取消喜欢楼中楼评论
@login_required
def delike_intercomment(request, intercomment_id):
    intercomment = InterComment.objects.get(id=intercomment_id)
    judge_activate(intercomment.extercomment.blogpost, POST_MESSAGE)
    judge_activate(intercomment, COMMENT_MESSAGE)

    post_id = intercomment.exter_comment.blogpost.id
    intercomment.like_user.remove(request.user.id)
    intercomment.like_num = len(intercomment.like_user.all())
    intercomment.save()
    return redirect('blogs:blogpost', post_id)

# 删除楼中楼评论
@login_required
def del_intercomment(request, intercomment_id):
    intercomment = InterComment.objects.get(id=intercomment_id)
    judge_activate(intercomment.extercomment.blogpost, POST_MESSAGE)
    judge_activate(intercomment, COMMENT_MESSAGE)
    if intercomment.owner.id != request.user.id:
        raise Http404

    post_id = intercomment.exter_comment.blogpost.id
    intercomment.activate = False
    intercomment.save()
    change_commentnum(post_id)
    return redirect('blogs:blogpost', post_id)