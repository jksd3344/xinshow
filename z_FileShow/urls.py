#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import patterns, url
from z_FileShow import views

urlpatterns = patterns(' ',
		url(r'^show/$',views.show,name='show'),
		url(r'^File_detach/$',views.File_detach,name='File_detach'),
		url(r'^dele_file/$',views.dele_file,name='dele_file')
	)