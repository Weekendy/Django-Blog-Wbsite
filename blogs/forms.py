from django import forms
from .models import Tag, BlogPost, BlogPostComment, InterComment, BlogPostMedia

# 新建标签表单
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['text']
        labels = {'text': '标签'}

# 新建媒体表单
class BlogPostMediaform(forms.ModelForm):
    class Meta:
        model = BlogPostMedia
        fields = ['image']
        labels = {'image': '选择图片上传'}

# 新建博客帖子表单
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'text']
        labels = {'title': '标题', 'text': '内容'}
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80,},)
        }


# 新建博客帖子评论表单
class BlogPostCommentForm(forms.ModelForm):
    class Meta:
        model = BlogPostComment
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols':50, 'resize': 'none'})}

# 新建楼中楼评论表单
class InterCommentForm(forms.ModelForm):
    class Meta:
        model = InterComment
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols':5, 'resize': 'none'})}