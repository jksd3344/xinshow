#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import patterns, url
from z_ReFile import views

urlpatterns = [
		url(r'^index/$',views.index,name='index'),
		url(r'^regist/$',views.regist,name='regist'),
		url(r'^login/$',views.login,name='login'),
		url(r'^takemassage/$',views.takemassage,name='takemassage'),
		url(r'^Runmsg/(\d+)/$',views.Runmsg,name='Runmsg'),
		url(r'^delmsg/$',views.delmsg,name='delmsg'),
	]