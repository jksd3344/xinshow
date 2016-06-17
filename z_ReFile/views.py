# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import datetime
import subprocess
import random
from model import Pmsg
from model import feed_list
from django.shortcuts import render
from django.http import HttpResponse
fs=feed_list()
Pmsg=Pmsg()
import logging
logger = logging.getLogger('all_project')
logger.info('aaa')


class JsonRes(HttpResponse):
    def __init__(self,
            content={},
            status=None,
            content_type='application/json'):

        super(JsonRes, self).__init__(
            json.dumps(content),
            status=status,
            content_type=content_type)


'''注册----------------------------------------------------------------------(未完成)-'''
def regist(request):
	if request.method=='POST':
		username           =  request.POST.get("username","")
		department        =  request.POST.get("department","")
		passward            =  request.POST.get("passward","")
		passwardagain   =  request.POST.get("passwardagain","")
		print("s=%s"%{"username":username,"department":department,"passward":passward,"passwardagain":passwardagain})
		start=200
		return JsonRes(json.dumps(start))
	else:
		return render(request,"z_ReFile/regist.html")

'''登陆'''
def login(request):
	return render(request,"z_ReFile/login.html")
'''---------------------------------------------------------------------------------'''




'''首页(page)'''
def index(request):
	return render(request,"z_ReFile/index.html")

'''任务列表页(page)'''
def Runmsg(request,pageid):
	data,totolpage,pageid=fs.feedgo_showmsg(int(pageid))
	for i in data:
		i["Stime"] = i["Stime"].strftime("%Y-%m-%d")
		i["Etime"] = i["Etime"].strftime("%Y-%m-%d")
	show = {"data":data,"totolpage":totolpage,"pageid":pageid}
	return render(request,"z_ReFile/Runmsg.html",show)

'''删除'''
def delmsg(request):
	delid=request.POST.get("delid","")
	Pmsg.feedgo_delmsg(delid)
	start=200
	return JsonRes(json.dumps(start))

'''任务提交(ajax)'''
def takemassage(request):
	Stime       = request.POST.get("Stime","")
	Etime       = request.POST.get("Etime","")
	ucid         = request.POST.get("ucid","")
	oid           = request.POST.get("oid","'").split(",")
	Remarks  = request.POST.get("Remarks","'")
	Stime       = datetime.datetime.strptime(Stime,"%Y-%m-%d")
	Etime       = datetime.datetime.strptime(Etime,"%Y-%m-%d")
	data         = {}
	start         = 0
	usetime   = 0
	utime       = 0
	Power      = 100
	st             = Stime.strftime("%Y-%m-%d")
	et             = Etime.strftime("%Y-%m-%d")

	#如果结束日期小于开始日期则错误
	if (Etime-Stime).days < 0:
		start=500
		return JsonRes(json.dumps(start))
	usetime=(Etime-Stime).days+1

	# 如果提交太多进程则错误
	if len(oid)>20:
		start=300
		return JsonRes(json.dumps(start))

	# 获取规则id
	ruleid=Pmsg.rule_calculation(st,et)
	if ruleid==1:
		usetime=usetime*2*len(oid)*2
	elif ruleid==2:
		usetime=usetime*3*len(oid)*2
	elif ruleid==3:
		usetime=usetime*3*len(oid)*2

	#如果主机已到最高负载则错误
	# hostid = Pmsg.Power_calculation(Power,hostnum=3)
	hostid=random.randint(1, 3)
	# hostid=1
	oid=','.join(oid)
	

	data={
		"Stime":Stime,#开始时间
		"Etime":Etime,#结束时间
		"ucid":ucid,#ucid
		"oid":oid,#oid
		"Whether":0,#是否结束
		"Remarks":Remarks,#备注
		"startprogress":usetime,#start进度
		"comprogress":0,#com进度
		"hostid":str(hostid)
	}
	userid=Pmsg.feedgo_createspeed(data)
	# 50 "/home/zzg/feed_tool/xinshow/z_ReFile/takeshow.py",
	# "/usr/local/apache2/htdocs/xinshow/z_ReFile/takeshow.py",
	# "/home/itcast/0420text/djantext/xinshow/z_ReFile/takeshow.py",
	cmd = "python /home/itcast/0420text/djangoTest/xinshow/z_ReFile/takeshow.py %s %s %s %s %s %s %s"%(Stime.strftime("%Y-%m-%d"),Etime.strftime("%Y-%m-%d"),ucid,oid,userid,hostid,str(ruleid))
	subprocess.Popen([
		"python",
		# "/home/itcast/0420text/djantext/sxinshwo/xinshow/z_ReFile/takeshow.py",
		"/usr/local/apache2/htdocs/xinshow/z_ReFile/takeshow.py",
		Stime.strftime("%Y-%m-%d"),
		Etime.strftime("%Y-%m-%d"),
		ucid,
		oid,
		userid,
		str(hostid),
		str(ruleid),
	])
	print("cmd??=%s"%cmd)
	logger.info('cmd=%s'%cmd)
	start=200
	return JsonRes(json.dumps(start))



