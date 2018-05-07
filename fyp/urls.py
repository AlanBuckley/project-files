"""fyp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include
from fyp_project import views

urlpatterns = [
    path('', include('fyp_project.urls')),
    path('fyp_project/', include('fyp_project.urls')),
    path('admin/', admin.site.urls),
    path('fyp_project/login/', views.login, name ='login'),
    path('fyp_project/signup/', views.signup, name ='signup'),
    path('fyp_project/homepage/', views.homepage, name='homepage'),
    path('fyp_project/Cyberbullying_info/', views.Cyberbullying_info, name='Cyberbullying_info'),
    path('fyp_project/emotionalHealthInfo/', views.emotionalHealthInfo, name='emotionalHealthInfo'),
    path('fyp_project/about/', views.about, name='about'),
    path('fyp_project/logout/', views.logout, name='logout'),
    path('fyp_project/profile/', views.profile, name ='profile'),
    path('fyp_project/editProfile/', views.editProfile, name='editProfile'),
    path('fyp_project/changePassword/', views.changePassword, name = 'changePassword'),
]
