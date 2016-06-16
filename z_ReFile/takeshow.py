# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import signal
import Queue
import paramiko
import MySQLdb
import subprocess
import datetime,time
from multiprocessing import Pool
db_show = MySQLdb.connect(host="123.57.226.182",user="root",passwd="Jksd3344",db="Shake",charset="utf8")   
db = db_show.cursor()


'''定义脚本输出类'''
class TakeShow(object):
	def __init__(self):
		self.pat            = []
		self.oid            = ""
		self.uid            = ""
		self.ucid           = ""
		self.Stime          = ""
		self.Etime          = ""
		self.ShowDays    = datetime.datetime.now()
		self.bin1            = "/home/zzg/coopinion/lemur-4.11/site-search/oopin_cgi_ctr_v2/bin"
		self.bin2            = "/home/zzg/coopinion/lemur-4.11/site-search/oopin_cgi_ctr_v2/bin_1"
		self.bin3           = "/home/zzg/coopinion/lemur-4.11/site-search/oopin_cgi_ctr_v2/bin_2"
		self.sqlcom       = ""
		self.sqlwh          = "update feedgo set Whether=1 where userid=%s"
		self.hostid         = 0
		self.ruleid         = 0
		self.host1          = {}
		self.host2          = {}
		self.host3          = {}
		self.cmd1          = ""
		self.cmd2          = ""
		self.cmd3          = ""
		self.filename    = "z_ReFile/filelog.txt"
		self.p                 = Pool(10)
	


	'''初始化参数'''
	def TakePat(self):
		try:
			self.pat     = sys.argv
			self.Stime   = (self.pat)[1]
			self.Etime   = (self.pat)[2]
			self.ucid    = (self.pat)[3]
			self.oid     = (self.pat)[4]
			self.uid     = (self.pat)[5]
			self.hostid  = int((self.pat)[6])
			self.ruleid  = int((self.pat)[7])
			self.sqlwh   = self.sqlwh%(self.uid)	
			self.host1   = {"host_":"123.57.226.182","port_":22,"username":"root","password":"Jksd3344","cmd":""}
			self.host2   = {"host_":"123.57.226.182","port_":22,"username":"root","password":"Jksd3344","cmd":""}
			self.host3   = {"host_":"123.57.226.182","port_":22,"username":"root","password":"Jksd3344","cmd":""}
			# self.host1   = {"host_":"192.168.241.50","port_":17717,"username":"zzg","password":"hZ4o7ZpG888","cmd":""}
			# self.host2   = {"host_":"192.168.241.18","port_":17717,"username":"zzg","password":"hZ4o7ZpG888","cmd":""}
			# self.host3   = {"host_":"192.168.241.17","port_":17717,"username":"zzg","password":"hZ4o7ZpG888","cmd":""}
		except Exception,e:
			print "unknow parameter"
			print "python take_file 'filename'"
			exit()

	'''脚本ssh登录执行功能'''
	def remote_execute(self,hostmsg):
		talk=[];cmdtale="cmd=%s\n"%hostmsg.get("cmd","")
		print(cmdtale)

		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(
			hostmsg.get("host_",""),
			port = hostmsg.get("port_",""),
			username = hostmsg.get("username",""),
			password = hostmsg.get("password",""),
			)
		stdin,stdout,stderr = client.exec_command(hostmsg.get("cmd",""))
		for i in stdout:
			print("go=%s\n"%i)
		return stdout


	'''不同规则需要的执行策略'''
	def rule_action(self,ruleid,host):
		if ruleid==1:
			# 先执行bin文件
			host["cmd"]=self.cmd1
			self.p.apply_async(remote_execute,args=(host,))
			# 在执行bin_1文件
			host["cmd"]=self.cmd2
			self.p.apply_async(remote_execute,args=(host,))
			# 需要执行不同的sql语句
			self.sqlcom = "update feedgo set comprogress=(comprogress+%s) where userid=%s"%("2",self.uid)
		elif ruleid ==2:
			# 执行bin_3文件
			host["cmd"]=self.cmd3
			self.p.apply_async(remote_execute,args=(host,))
			sqlcom = "update feedgo set comprogress=(comprogress+%s) where userid=%s"%("1",self.uid)
		elif ruleid ==3:
			#执行全部文件
			host["cmd"]=self.cmd1
			self.p.apply_async(remote_execute,args=(host,))
			host["cmd"]=self.cmd2
			self.p.apply_async(remote_execute,args=(host,))
			host["cmd"]=self.cmd3
			self.p.apply_async(remote_execute,args=(host,))
			self.sqlcom = "update feedgo set comprogress=(comprogress+%s) where userid=%s"%("3",self.uid)
		return 0


	def hosid_show(self):
		print("ss")
		if self.hostid==1:
			self.rule_action(self.ruleid,self.host1)
		elif self.hostid==2:
			self.rule_action(self.ruleid,self.host2)
		elif self.hostid==3:
			self.rule_action(self.ruleid,self.host3)


	'''执行计划'''
	def ImpmentSp(self):
		self.TakePat()
		# self.sig_show()

		talk="start________________________________________\n"
		print("talk=%s"%talk)

		Stime    = datetime.datetime.strptime(self.Stime,"%Y-%m-%d")
		Etime    = datetime.datetime.strptime(self.Etime,"%Y-%m-%d")
		difdays = (Etime-Stime).days
		self.oid = self.oid.split(',')
	
		# 执行次数为日期之差
		for i in range(difdays+1):
			days = datetime.timedelta(days=i)
			self.ShowDays = (Etime-days).strftime("%Y-%m-%d")

			talk="%s:success\n"%self.ShowDays
			print("talk=%s"%talk)

			if self.oid==["0"]:
				# self.cmd1= "cd %s;./adhoc_ctr_feeding 1 %s %s"%(self.bin1,str(self.ucid),str(self.ShowDays))
				# self.cmd2= "cd %s;./adhoc_ctr_feeding 1 %s %s"%(self.bin2,str(self.ucid),str(self.ShowDays))
				# self.cmd3= "cd %s;./adhoc_ctr_feeding 1 %s %s"%(self.bin3,str(self.ucid),str(self.ShowDays))
				self.cmd1= "cd /home/itcast/testy;./sleepTest.o %s"%str(self.ShowDays)
				self.cmd2= "cd /home/itcast/testy;./sleepTest.o %s"%str(self.ShowDays)
				self.cmd3= "cd /home/itcast/testy;./sleepTest.o %s"%str(self.ShowDays)

				# 通过hostid确定执行的命令和主机ip
				self.hosid_show()
			else:
				for i in self.oid:
					# self.cmd1= "cd %s;./adhoc_ctr_feeding 1 %s %s %s"%(self.bin1,str(self.ucid),str(self.ShowDays),str(i))
					# self.cmd2= "cd %s;./adhoc_ctr_feeding 1 %s %s %s"%(self.bin2,str(self.ucid),str(self.ShowDays),str(i))
					# self.cmd3= "cd %s;./adhoc_ctr_feeding 1 %s %s %s"%(self.bin3,str(self.ucid),str(self.ShowDays),str(i))
					self.cmd1= "cd /home/itcast/testy;./sleepTest.o %s"%str(self.ShowDays)
					self.cmd2= "cd /home/itcast/testy;./sleepTest.o %s"%str(self.ShowDays)
					self.cmd3= "cd /home/itcast/testy;./sleepTest.o %s"%str(self.ShowDays)
					
					# 通过hostid确定执行的命令和主机ip
					self.hosid_show()


			com = db.execute(self.sqlcom)
			db_show.commit()

		wh=db.execute(self.sqlwh)
		db.close() 

		self.p.close()
		self.p.join()
		talk="id:%s:--------End--------\n"%self.uid
		print(talk)


	'''信号阻断处理'''
	def sig_show(self):
		signal.signal(signal.SIGINT,self.reprogress)
		signal.signal(signal.SIGCHLD,self.reprogress)

	def reprogress(a,b):
		time=datetime.datetime.now().strftime("%Y-%m-%d,%H:%M:%S")
		sigtalk="%s:   :%s号信号处理信息被阻断,在处理之前您的进度已达到%s\n"%(time,a,self.ShowDays)
		print(sigtalk)


'''脚本ssh登录执行功能'''
def remote_execute(hostmsg):
	talk=[];cmdtale="cmd=%s\n"%hostmsg.get("cmd","")
	print(cmdtale)

	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(
		hostmsg.get("host_",""),
		port = hostmsg.get("port_",""),
		username = hostmsg.get("username",""),
		password = hostmsg.get("password",""),
		)
	stdin,stdout,stderr = client.exec_command(hostmsg.get("cmd",""))
	for i in stdout:
		print("go=%s\n"%i)
	return stdout


def ps(x):
	print("ssss")

if __name__=='__main__':
	Ts=TakeShow()
	Ts.ImpmentSp()
	db_show.commit()
	db_show.close()
	
