# !/usr/bin/env python
# -*- coding:utf-8 -*-


import random
import MySQLdb
from _models.models import feedgo
db_show = MySQLdb.connect(host="123.57.226.182",user="root",passwd="Jksd3344",db="Shake",charset="utf8")   
db = db_show.cursor()  

class Pmsg(object):
	def __init__(self):
		self.hostid=0
		self.suc=200
		self.err=500
		self.sql="SELECT SUM(%s) FROM feedgo WHERE Whether=0 AND hostid=%s"
	
	#存储表
	def feedgo_createspeed(self,data):
		userid=str(random.randint(1,10000))
		show = feedgo.objects.create(
			userid=userid,
			Stime=data.get("Stime",""),#是否结束
			Etime=data.get("Etime",""),#备注
			Whether=data.get("Whether",""),#是否结束
			Remarks=data.get("Remarks",""),#备注
			ucid=data.get("ucid",""),#ucid
			oid=data.get("oid",""),#oid
			startprogress=data.get("startprogress",""),
			comprogress=data.get("comprogress",""),
			hostid=data.get("hostid","")
			)
		return userid
	
	#遍历表
	def feedgo_showmsg(self):
		data = feedgo.objects.all().values()
		return data

	#对返回数据进行处理
	def take_sql(self,sql):
		data=0
		db.execute(sql)
		for i in db.fetchall():
			data=list(i)[0]
			if data==None:
				data=0
		return data

	#查询单一机器负载数量 执行量/总量
	def Power_calculations(self,Power,usetime,hostid):
		data=0
		strpro=0
		compro=0
		sqlstrpro=self.sql%("startprogress",hostid)
		sqlcompro = self.sql%("comprogress",hostid)
		strpro=self.take_sql(sqlstrpro)
		compro=self.take_sql(sqlcompro)	
		data = strpro-compro
		if data>Power and (Power-data)<usetime:
			return self.err
		else:
			self.hostid=hostid
			return self.suc

	#循环查询负载量
	def Power_calculation(self,Power,usetime,hostnum):
		data=0;start=0
		for i in range(hostnum):
			data=self.Power_calculations(Power,usetime,hostid=(i+1))
			if data==self.suc:
				return self.hostid	

		if data==self.err:
			return self.err

