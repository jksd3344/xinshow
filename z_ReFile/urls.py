#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import patterns, url
from z_ReFile import views

urlpatterns = patterns(' ',
		url(r'^index/$',views.index,name='index'),
		url(r'^takemassage/$',views.takemassage,name='takemassage'),
		url(r'^Runmsg/(\d+)/$',views.Runmsg,name='Runmsg'),
		url(r'^delmsg/$',views.delmsg,name='delmsg'),
	)