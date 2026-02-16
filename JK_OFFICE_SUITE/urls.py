"""
URL configuration for JK_OFFICE_SUITE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.shortcuts import render
from django.contrib import admin

urlpatterns = [
    path('', lambda request: render(request, 'Authentication/homepage.html'), name='home'),
    path('auth/', include('Authentication.urls')),
    path('Director/', include('Director.urls')),
    path('HR/', include('HR.urls')),
    path('auth/Manager/', include('Manager.urls')),
    path('Staff/', include('Staff.urls')),
    path('admin/', admin.site.urls),
]
