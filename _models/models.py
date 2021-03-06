# !/usr/bin/env python
# -*- coding:utf-8 -*-

from django.db import models


# Create your models here.
class feedgo(models.Model):
    id = models.BigIntegerField(primary_key=True)
    userid=models.IntegerField(blank=True,null=False)#进度
    Stime=models.CharField(unique=True,max_length=32) #开始时间
    Etime=models.CharField(unique=True,max_length=32) #结束时间
    Whether=models.IntegerField(blank=True,null=True)  #是否结束
    Remarks=models.CharField(unique=True,max_length=32) #备注
    ucid=models.IntegerField(blank=True,null=True) #ucid
    oid=models.CharField(unique=True,max_length=200)  #oid
    startprogress=models.IntegerField(blank=True,null=True)#进度
    comprogress=models.IntegerField(blank=True,null=True)#进度
    hostid=models.IntegerField(blank=True,null=False)#进度

    class Meta:
    	managed = False
    	db_table="feedgo"


