"""bighg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from apps.web.views import rsa
from apps.web.views import server
from apps.web.views import project
from apps.web.views import deploy

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^rsa/list/$', rsa.rsa_list, name='rsa_list'),
    url(r'^rsa/add/$', rsa.rsa_add, name='rsa_add'),
    url(r'^rsa/edit/(?P<pk>\d+)/$', rsa.rsa_edit, name='rsa_edit'),
    url(r'^rsa/del/(?P<pk>\d+)/$', rsa.rsa_del, name='rsa_del'),

    url(r'^server/list/$', server.server_list, name='server_list'),
    url(r'^server/add/$', server.server_add, name='server_add'),
    url(r'^server/edit/(?P<pk>\d+)/$', server.server_edit, name='server_edit'),
    url(r'^server/del/(?P<pk>\d+)/$', server.server_del, name='server_del'),

    url(r'^project/list/$', project.project_list, name='project_list'),
    url(r'^project/add/$', project.project_add, name='project_add'),
    url(r'^project/edit/(?P<pk>\d+)/$', project.project_edit, name='project_edit'),
    url(r'^project/del/(?P<pk>\d+)/$', project.project_del, name='project_del'),

    url(r'^env/list/$', project.project_env_list, name='project_env_list'),
    url(r'^env/add/$', project.project_env_add, name='project_env_add'),
    url(r'^env/edit/(?P<pk>\d+)/$', project.project_env_edit, name='project_env_edit'),
    url(r'^env/del/(?P<pk>\d+)/$', project.project_env_del, name='project_env_del'),

    url(r'^env/task/list/(?P<env_id>\d+)/$', deploy.deploy_task_list, name='deploy_task_list'),
    url(r'^env/task/add/(?P<env_id>\d+)/$', deploy.deploy_task_add, name='deploy_task_add'),
    url(r'^env/task/del/(?P<pk>\d+)/$', deploy.deploy_task_del, name='deploy_task_del'),

    url(r'^git/commits/$', deploy.git_commits, name='git_commits'),
    url(r'^get/script/template/(?P<template_id>\d+)/$', deploy.get_script_template, name='get_script_template'),

    url(r'^env/channels/deploy/(?P<task_id>\d+)/$', deploy.channels_deploy, name='channels_deploy'),

    url(r'^', rsa.rsa_list, name='index'),

]
