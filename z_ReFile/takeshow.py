# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import Queue
import MySQLdb
import subprocess
import datetime,time
db_show = MySQLdb.connect(host="123.57.226.182",user="root",passwd="Jksd3344",db="Shake",charset="utf8")   
db = db_show.cursor()  

'''定义脚本输出类'''
class TakeShow(object):
	def __init__(self):
		self.pat             = []
		self.oid             = ""
		self.uid             = ""
		self.ucid           = ""
		self.Stime         = ""
		self.Etime         = ""
		self.ShowDays = datetime.datetime.now()
		self.bin0           = "/home/zzg/coopinion/lemur-4.11/site-search/oopin_cgi_ctr_v2/bin"
		self.bin1           = "/home/zzg/coopinion/lemur-4.11/site-search/oopin_cgi_ctr_v2/bin_1"
		self.bin2           = "/home/zzg/coopinion/lemur-4.11/site-search/oopin_cgi_ctr_v2/bin_2"
		self.sqlcom       = "update feedgo set comprogress=(comprogress+1) where userid=%s"
		self.sqlwh         = "update feedgo set Whether=1 where userid=%s"

	'''初始化参数'''
	def TakePat(self):
		try:
			self.pat       = sys.argv
			self.Stime   = (self.pat)[1]
			self.Etime   = (self.pat)[2]
			self.ucid     = (self.pat)[3]
			self.oid       = (self.pat)[4]
			self.uid       = (self.pat)[5]
			self.sqlcom = self.sqlcom%(self.uid)
			self.sqlwh   = self.sqlwh%(self.uid)

		except Exception,e:
			print "unknow parameter"
			print "python take_file 'filename'"
			exit()

	'''执行计划'''
	def ImpmentSp(self):
		self.TakePat()

		Stime    = datetime.datetime.strptime(self.Stime,"%Y-%m-%d")
		Etime    = datetime.datetime.strptime(self.Etime,"%Y-%m-%d")
		difdays = (Etime-Stime).days

		for i in range(difdays+1):
			print("ss")
			days = datetime.timedelta(days=i)
			self.ShowDays = (Etime-days).strftime("%Y-%m-%d")
			subprocess.call(['/home/itcast/0420text/djantext/xinshow/z_ReFile/sleepTest.o','1',str(self.ucid),str(self.ShowDays),str(self.oid)])
			com = db.execute(self.sqlcom)
			db_show.commit()

		wh=db.execute(self.sqlwh)
		db.close() 

if __name__=='__main__':
	Ts=TakeShow()
	Ts.ImpmentSp()
	db_show.commit()
	db_show.close()


