from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    
    path('user/<int:user_id>/', views.user, name="user"),
    path('edit_property/', views.edit_property, name='edit_property'),

    path('user/<int:user2_id>/follow/', views.follow, name="follow"),
    path('user/<int:user2_id>/defollow/', views.defollow, name="defollow"),
    path('user/<int:user_id>/follow_list/', views.follow_list, name='follow_list'),
    path('user/<int:user_id>/followed_list/', views.followed_list, name="followed_list"),

    path('user/<int:user_id>/mypost_list', views.mypost_list, name='mypost_list'),
    path('user/<int:user_id>/likepost_list', views.likepost_list, name="likepost_list"),
    path('user/<int:user_id>/logpost_list', views.logpost_list, name='logpost_list'),
]