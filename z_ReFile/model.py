# !/usr/bin/env python
# -*- coding:utf-8 -*-


import random
import MySQLdb
from _models.models import feedgo
db_show = MySQLdb.connect(host="123.57.226.182",user="root",passwd="Jksd3344",db="Shake",charset="utf8")   
db = db_show.cursor()  

class Pmsg(object):

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
			comprogress=data.get("comprogress","")
			)
		return userid

	def feedgo_showmsg(self):
		data = feedgo.objects.all().values()
		return data

	def take_sql(self,sql):
		data=0
		db.execute(sql)
		for i in db.fetchall():
			data=list(i)[0]
			if data==None:
				data=0
		return data

	def Power_calculation(self,Power):
		start=0
		data=0
		strpro=0
		compro=0
		sqlstrpro   = "SELECT SUM(startprogress) FROM feedgo WHERE Whether=0"
		sqlcompro = "SELECT SUM(comprogress) FROM feedgo WHERE Whether=0"

		strpro=self.take_sql(sqlstrpro)
		compro=self.take_sql(sqlcompro)

		data = strpro-compro
		print("data=%s"%data)
		if data>Power:
			return data
		else:
			start=200
			return start