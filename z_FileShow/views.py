#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
import json
import re

class JsonRes(HttpResponse):
    def __init__(self,
            content={},
            status=None,
            content_type='application/json'):

        super(JsonRes, self).__init__(
            json.dumps(content),
            status=status,
            content_type=content_type)

# 文件处理
class ApplicationClass(object):
	def __init__(self):
		#初始化文件地址
		self.File_Name="/home/itcast/0420text/djantext/xinshow/ds_seed.dat"
		self.n=0

	#每次读一行返回列表
	def read_line(self):
		num = {};N= self.n;
		filr_w = [];File_Path=[];
		TestFile = open(self.File_Name,'r')
		
		while(1):
			line = TestFile.readline().strip('\n')
			TestFile.flush()
			if not line:
				break
			N=N+1
			File_Path.append({
				"n":N,
				"line":line
			})
			filr_w.append(line)
		self.n=N
		print("n=%s"%N)
		TestFile.close()
		return File_Path,filr_w
	
	#写入文件
	def write_some(self,file):
		TestFile = open(self.File_Name,'w')
		TestFile.write(file)
		TestFile.close()
		return 1

	#删除指定一行
	def File_delete_line(self,Num):
		filr_w = []
		TestFile = open(self.File_Name,'r')
		n = self.n
		while(1):
			line = TestFile.readline().strip('\n')
			TestFile.flush()
			if not line:
				break
			n=n+1
			if n==Num:
				print("delete=%sline"%n)
			else:
				filr_w.append(line)

		TestFile.close()
		return filr_w
#读入文件
def show(request):
	size = 10
	faction = ApplicationClass()
	filr_w,fa = faction.read_line()
	resp_json = {'File_Path':filr_w}
	return render(request,'z_FileShow/index.html',resp_json)

# 66873,66865;https://detail.tmall.com/item.htm?id=38607934101
def File_detach(request):
	#获取urls
	urls = request.POST.get("file_url","")
	#初始化错误号,	初始化正则
	show=0;s_urls = r'(.*?\;)(https://.*)'
	#多条处理
	list_url = urls.split('\n');	list_gurl = []

	# 多条遍历正则普配,匹配成功放入list_gurl,失败返回500
	for i in range(len(list_url)):
		urls_obj = re.search(s_urls,list_url[i].encode())
		if urls_obj is not None:
			if cmp(list_url[i].encode(),urls_obj.group())==0:
				list_gurl.append(urls_obj.group())
				# print("s_urls%s"%urls_obj.group())
			else:
				show=500
				return JsonRes(json.dumps(show))
		else:
			show=500
			return JsonRes(json.dumps(show))

	#列表转化为字符串"\n"
	uurl = '\n'.join(list_gurl)
	urls=uurl

	#读取文件加入urls并写入新文件
	faction = ApplicationClass()
	filr_w,fa = faction.read_line()
	fa.append(urls)
	fa = '\n'.join(fa)

	if faction.write_some(fa)==1:
		show = 200
		return JsonRes(json.dumps(show))

# 删除文件
def dele_file(request):
	num = int(request.POST.get("num","").encode())
	# 接收num
	faction = ApplicationClass()
	filr_w = faction.File_delete_line(num)
	filr_w = '\n'.join(filr_w)
	if faction.write_some(filr_w)==1:
		show=200
		return JsonRes(json.dumps(show))





