"""graduation_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from hosts import urls as hosts_urls
from hosts import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hosts/', include(hosts_urls)),   ##这里把hosts项目（app应用）当作一个子项目开发了
    url(r'^$', views.index, name='dashboard'),
    url(r'^hosts/', include(hosts_urls), name='hosts'),
    url(r'^login/', views.acc_login, name='login'),
    url(r'^logout/', views.acc_logout, name='logout'),

    url(r"^assets$", views.assets_index, name='assets'),
    url(r"^monitor$", views.monitor_index, name='monitor'),
]
