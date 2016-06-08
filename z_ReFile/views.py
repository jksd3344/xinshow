# !/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import datetime
import subprocess
from model import Pmsg
from django.shortcuts import render
from django.http import HttpResponse
Pmsg=Pmsg()


class JsonRes(HttpResponse):
    def __init__(self,
            content={},
            status=None,
            content_type='application/json'):

        super(JsonRes, self).__init__(
            json.dumps(content),
            status=status,
            content_type=content_type)	

'''首页(page)'''
def index(request):
	return render(request,"z_ReFile/index.html")

'''任务列表页(page)'''
def Runmsg(request):
	data=Pmsg.feedgo_showmsg()
	for i in data:
		i["Stime"] = i["Stime"].strftime("%Y-%m-%d")
		i["Etime"] = i["Etime"].strftime("%Y-%m-%d")
	show = {"data":data}
	return render(request,"z_ReFile/Runmsg.html",show)

'''任务提交(ajax)'''
def takemassage(request):
	Stime       = request.POST.get("Stime","")
	Etime       = request.POST.get("Etime","")
	ucid         = request.POST.get("ucid","")
	oid           = request.POST.get("oid","'")
	Remarks  = request.POST.get("Remarks","'")
	Stime       = datetime.datetime.strptime(Stime,"%Y-%m-%d")
	Etime       = datetime.datetime.strptime(Etime,"%Y-%m-%d")
	data         = {}
	start         = 0
	usetime   = 0
	Power      = 50

	if (Etime-Stime).days < 0:
		start=500
		return JsonRes(json.dumps(start))

	data = Pmsg.Power_calculation(Power)
	# if not data==200:
	# 	return JsonRes(json.dumps(start))

	usetime=(Etime-Stime).days+1
	data={
		"Stime":Stime,#开始时间
		"Etime":Etime,#结束时间
		"ucid":ucid,#ucid
		"oid":oid,#oid
		"Whether":0,#是否结束
		"Remarks":Remarks,#备注
		"startprogress":usetime,#start进度
		"comprogress":0,#com进度
	}
	userid=Pmsg.feedgo_createspeed(data)

	cmd = "python /home/itcast/0420text/djantext/xinshow/z_ReFile/takeshow.py %s %s %s %s %s"%(Stime.strftime("%Y-%m-%d"),Etime.strftime("%Y-%m-%d"),ucid,oid,userid),
	subprocess.Popen([
		"python",
		"/home/itcast/0420text/djantext/xinshow/z_ReFile/takeshow.py",
		Stime.strftime("%Y-%m-%d"),
		Etime.strftime("%Y-%m-%d"),
		ucid,
		oid,
		userid,

	])
	print("cmd%s"%cmd)
	start=200
	return JsonRes(json.dumps(start))



