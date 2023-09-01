from django.contrib import admin
from .models import *

admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(BlogPostComment)
admin.site.register(InterComment)
admin.site.register(Tag)
admin.site.register(BlogPostMedia)
admin.site.register(LikeBlogPost)