#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.db import models
from django.db import models

# Create your models here.
class feedgo(models.Model):
    id = models.BigIntegerField(primary_key=True)
    Stime=models.CharField(unique=True,max_length=32) #开始时间
    Etime=models.CharField(unique=True,max_length=32) #结束时间
    Whether=models.CharField(unique=True,max_length=32) #是否时间
    Remarks=models.CharField(unique=True,max_length=32) #备注
    ucid=models.IntegerField(blank=True,null=True) #ucid
    oid=models.IntegerField(blank=True,null=True) #oid
    setbacks=models.IntegerField(blank=True,null=True)#进度

    class Meta:
    	managed = False
    	db_table="feedgo"


