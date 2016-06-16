# !/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import random
import datetime
import MySQLdb
from math import ceil,floor
from _models.models import feedgo
db_show = MySQLdb.connect(host="123.57.226.182",user="root",passwd="Jksd3344",db="Shake",charset="utf8")   
db = db_show.cursor()  

class Pmsg(object):

	# 初始化数据
	'''
		ruleid:规则id
		hostid:主机ip
		suc:成功返回
		err:失败返回

	'''
	def __init__(self):
		self.ruleid=0
		self.hostid=0
		self.suc=200
		self.err=500
		self.sql="SELECT count(*) FROM feedgo WHERE Whether=0"

	#存储表
	def feedgo_createspeed(self,data):
		userid=str(random.randint(1,10000))+str(datetime.datetime.now().strftime("%Y"))
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
		num=feedgo.objects.all().count()
		pnu=2
		liannu=5
		print("num=%s"%num)

		sh=showpage(num,pnu,liannu)
		da=sh.page_show(1)
		print("da=%s"%da)
		return data

	#删除指定元素
	def feedgo_delmsg(self,delid):
		data = feedgo.objects.get(id=delid).delete()
		return self.suc


	# 对返回数据进行处理
	def take_sql(self,sql):
		data=0
		db.execute(sql)
		for i in db.fetchall():
			data=list(i)[0]
			if data==None:
				data=0
		return data

	# 查询单一机器负载数量 执行量/总量
	def Power_calculations(self,Power,hostid):
		strpro=0
		strpro=self.take_sql(self.sql)
		if strpro>Power:
			return self.err
		else:
			self.hostid=hostid
			return self.suc


	# 循环查询负载量
	'''
		Power:一台主机可承受的负载量
		hostnum:主机数量
	'''
	def Power_calculation(self,Power,hostnum):
		data=0;start=0
		for i in range(hostnum):
			data=self.Power_calculations(Power,hostid=(i+1))
			if data==self.suc:
				return self.hostid	

		if data==self.err:
			return self.err



	#查询负载量之前必须先确定调用的时间与机器
	'''
		ruleid==1调用本周之内的时间(bin,bin_1)
		ruleid=2调用本周之外的时间(bin2)
		ruleid=3包含本周之内与本周之外的时间(bin3)
	'''
	def rule_calculation(self,Stime,Etime):
		noweek=time.strftime("%W") # 当前周
		sweek=time.strftime("%W",time.strptime(Stime,"%Y-%m-%d")) #获取周
		eweek=time.strftime("%W",time.strptime(Etime,"%Y-%m-%d")) #获取周
		if cmp(noweek,sweek)==0 and cmp(noweek,eweek)==0:
			self.ruleid=1
			# 策略id为1 当时间为本周内时 执行bin，bin_1 执行两个文件
		elif cmp(noweek,sweek)!=0 and cmp(noweek,eweek)!=0:
			self.ruleid=2
			# 策略id为2 当时间为本周外时 执行bin2 执行1个文件
		elif cmp(noweek,sweek)!=0 and cmp(noweek,eweek)==0:
			self.ruleid=3
			# 策略id为3 当时间跨周时 执行bin1，bin2,bin3 执行3个文件
		return self.ruleid



# 返回分页数据
class feed_list(object):
	'''
		pagenu:每页显示条数
		linenum:每页显示链接数(未启用)
	'''
	def __init__(self):
		self.pagenu=8
		self.linenum=5
		self.suc=200
		self.err=500		

	def feedgo_showmsg(self,pageid):
		num=feedgo.objects.all().count()
		sh=showpage(num,self.pagenu,self.linenum)
		totolpage=sh.judge()
		if pageid>totolpage:
			pageid=1
		top=[]
		for i in range(totolpage):
			top.append(i+1)
		da=sh.page_show(pageid)
		data = feedgo.objects.all().order_by('-id').values()[da.start:da.end]
		return data,top,pageid


# 分页
class showpage(object):
	# 初始化数据
	'''
		total_records: 总条数
		perpage:         每页条数
		linesize:          每页链接数
		totolpage:       计算得出的页数
		data:               计算出来的数据

	'''
	def __init__(self,total_records,perpage,linesize):
		self.total_records=total_records
		self.perpage=perpage
		self.finnum=linesize
		self.totolpage=0
		self.data={}

	def judge(self):
		if self.total_records>self.perpage:
			self.totolpage=int(floor(self.total_records/float(self.perpage)))
			for i in range(self.totolpage):
				if i==0:
					self.data[i+1]=page(i+1,i,i+self.perpage,self)
				else:
					self.data[i+1]=page(i+1,self.data[i].end,self.data[i].end+self.perpage,self)
			if self.total_records%self.perpage!=0:
				# print("totolpage%s"%self.total_records,self.perpage)
				self.data[self.totolpage+1]=page(self.totolpage+1,self.data[self.totolpage].end,self.total_records,self)
				return self.totolpage+1
		else:
			self.totolpage=1
			self.data[1]=page(1,0,self.total_records,self)
		return self.totolpage

	def page_show(self,page_num):
		page_num=int(page_num)
		if page_num in self.data.keys():
			return self.data[page_num]
		else:
			return self.data[1]



class page(object):

	# 初始化数据
	'''
		pagenum:每页的页码
		start:每页的起始位置
		end:每页的结束位置
		nextpage:下一页
		prevpage:上一页
		showpage:showpage类

	'''
	def __init__(self,pagenum,start,end,showpage):
		self.pagenum=pagenum
		self.start=start
		self.end=end
		self.nextpage=self.pagenum+1
		self.prevpage=self.pagenum-1
		self.showpage=showpage







