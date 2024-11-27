from django.urls import path,include
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.member_menu, name='member_menu'),
    path('media-list-for-members/', views.media_list_for_members, name='media_list_for_members'),
]