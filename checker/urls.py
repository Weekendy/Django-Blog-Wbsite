from django.urls import path
from . import views

app_name = "checker"
urlpatterns = [
    path('blogpost_photo/', views.blogpost_photo, name='blogpost_photo')
]