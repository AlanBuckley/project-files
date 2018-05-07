from django.urls import path, include
from django.contrib import admin
from . import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    path('', login, {'template_name':'login.html'}),
    path('', views.login),
    path('', views.signup),
    path('', views.homepage),
    path('', views.Cyberbullying_info),
    path('', views.emotionalHealthInfo),
    path('', views.about),
    path('', logout, {'template_name':'logout.html'}),
    path('', views.logout),
    path('', views.profile),
    path('', views.editProfile),
    path('', views.changePassword),


]
