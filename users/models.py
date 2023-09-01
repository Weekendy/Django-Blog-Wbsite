from django.db import models
from django.contrib.auth.models import User
from blogs.models import BlogPost

# 用户头像媒体
class UserProfileMedia(models.Model):
    activate = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.OneToOneField(User, related_name='profile_media', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='images/user_porfile/', null=True, blank=True)
    
# 用户资料
class UserProperty(models.Model):
    user = models.OneToOneField(User, related_name='property', on_delete=models.CASCADE, null=True, blank=True)
    perweb = models.CharField(max_length=100, null=True, blank=True)
    introduce = models.CharField(max_length=16, default='这个人很懒，什么也没留下')
    sex = models.SmallIntegerField(choices=((0, '未知'), (1, '男'), (2, '女')), default=0)
    birthday = models.DateField(blank=True, null=True)
    follow = models.ManyToManyField('users.UserProperty', related_name='followed', blank=True)
    follow_num = models.IntegerField(default=0)
    followed_num = models.IntegerField(default=0)

    def __str__(self):
        return self.user.__str__() + "\'s property"

# 博客帖子浏览记录
class BlogWatchLog(models.Model):
    user_property = models.ForeignKey(UserProperty, on_delete=models.CASCADE, blank=True)
    blogpost = models.ForeignKey(BlogPost, on_delete=models.CASCADE, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date_added.__str__() + ', post=' + self.blogpost.__str__() + ', ' + self.user_property.user.__str__()

# 用户消息
class UserMessage(models.Model):
    is_readed = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='sended_message', on_delete=models.CASCADE, null=True, blank=True)
    to_user = models.ForeignKey(User, related_name='accepted_message', on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()

    def __str__(self):
        return self.text