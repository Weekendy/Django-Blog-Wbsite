from django.db import models
from django.contrib.auth.models import User

# 标签
class Tag(models.Model):
    activate = models.BooleanField(default=True)
    main = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)# 需用户输入
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.text
        


# 博客帖子
class BlogPost(models.Model):
    activate = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="blogposts", blank=True)# 需用户输入
    title = models.CharField(max_length=200) # 需用户输入
    text = models.TextField() # 需用户输入
    is_top = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    like_num = models.IntegerField(default=0)
    comment_num = models.IntegerField(default=0)
    image_num = models.IntegerField(default=0)

    def __str__(self):
        return self.title

# 喜欢的博客帖子
class LikeBlogPost(models.Model):
    blogpost = models.ForeignKey(BlogPost, related_name='like', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, related_name='like', on_delete=models.CASCADE, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date_added.__str__() + 'blogpost=' + self.blogpost.__str__() + ', ' + self.user.username



# 博客帖子媒体
class BlogPostMedia(models.Model):
    activate = models.BooleanField(default=False)# 需管理员审核后方可为True
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    blogpost = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/blogpost_photo/', null=True, blank=True)# 需用户输入

    def __str__(self):
        return self.date_added.__str__()



# 评论父类
class Comment(models.Model):
    activate = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField() # 需用户输入
    date_added = models.DateTimeField(auto_now_add=True)
    like_user = models.ManyToManyField(User, related_name="like_comment", verbose_name="点赞", blank=True)
    like_num = models.IntegerField(default=int(0))

    def __str__(self):
        if len(self.text) > 50:
            return self.text[:50] + '...'
        else:
            return self.text

# 博客帖子评论
class BlogPostComment(Comment):
    blogpost = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    floor_num = models.IntegerField()

# 博客帖子楼中楼评论
class InterComment(Comment):
    exter_comment = models.ForeignKey(BlogPostComment, on_delete=models.CASCADE)
    reflected_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)