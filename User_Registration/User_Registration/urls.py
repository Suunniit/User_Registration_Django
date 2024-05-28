"""
URL configuration for User_Registration project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', register, name='register'),
    path('user_login', user_login, name='user_login'),
    path('home', home, name='home'),
    path('user_profile', user_profile, name='user_profile'),
    path('user_logout', user_logout, name='user_logout'),
    path('otp', otp, name='otp'),
    path('cpass', cpass, name='cpass'),
    path('uname', uname, name='uname'),
    path('otp1', otp1, name='otp1'),
    path('fpass', fpass, name='fpass'),

    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
