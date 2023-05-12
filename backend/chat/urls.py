from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('auth/', views.auth_view, name='auth'),
    path('profile/', views.profile_view, name='profile'),
    path('chat/', views.messages_page, name='chat')

]