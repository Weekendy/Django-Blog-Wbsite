from django.urls import path
from . import views

app_name = 'blogs'
urlpatterns = [
    # 首页
    path('', views.index, name='index'),

    # 标签
    path('new_tag/', views.new_tag, name='new_tag'),
    path('tags/', views.tags, name='tags'),
    path('tag/<int:tag_id>', views.tag, name="tag"),
    path('add_tag/<int:post_id>', views.add_tag, name="add_tag"),
    path('unbind_tag/<int:post_id>/<int:tag_id>', views.unbind_tag, name="unbind_tag"),
  
    # 帖子
    path('new_blogpost/', views.new_blogpost, name='new_blogpost'),
    path('blogposts/', views.blogposts, name='blogposts'),
    path('blogpost/<int:post_id>', views.blogpost, name='blogpost'),
    path('edit_blogpost/<int:post_id>/', views.edit_blogpost, name='edit_blogpost'),
    path('like_blogpost/<int:post_id>', views.like_blogpost, name='like_blogpost'),
    path('delike_blogpost/<int:post_id>', views.delike_blogpost, name='delike_blogpost'),
    path('del_blogpost/<int:post_id>/', views.del_blogpost, name='del_blogpost'),
    
    #媒体
    path('add_photo/<int:post_id>', views.add_photo, name="add_photo"),
    path('del_photo/<int:media_id>', views.del_photo, name="del_photo"),

    # 博客帖子评论
    path('new_blogpostcomment/<int:post_id>', views.new_blogpostcomment, name="new_blogpostcomment"),
    path('like_blogpostcomment/<int:blogpost_comment_id>', views.like_blogpostcomment, name="like_blogpostcomment"),
    path('delike_blogpostcomment/<int:blogpost_comment_id>', views.delike_blogpostcomment, name="delike_blogpostcomment"),
    path('del_blogpostcomment/<int:blogpost_comment_id>', views.del_blogpostcomment, name="del_blogpostcomment"),
    
    # 楼中楼评论
    path('new_intercomment/<int:extercomment_id>', views.new_intercomment, name="new_intercomment"),
    path('new_intercomment2/<int:intercomment_id>', views.new_intercomment2, name="new_intercomment2"),
    path('like_intercomment/<int:intercomment_id>', views.like_intercomment, name="like_intercomment"),
    path('like_deintercomment/<int:intercomment_id>', views.delike_intercomment, name="delike_intercomment"),
    path('del_intercomment/<int:intercomment_id>', views.del_intercomment, name="del_intercomment"),
]