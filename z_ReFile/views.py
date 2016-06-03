from django.shortcuts import render
from django.http import HttpResponse
import json
# Create your views here.

class JsonRes(HttpResponse):
    def __init__(self,
            content={},
            status=None,
            content_type='application/json'):

        super(JsonRes, self).__init__(
            json.dumps(content),
            status=status,
            content_type=content_type)

def index(request):
	ReFile = {"hello":"hello"}
	return render(request,"z_ReFile/index.html",ReFile)


def takemassage(request):
	Stime = request.POST.get("Stime","")
	Etime = request.POST.get("Etime","")
	ucid   = request.POST.get("ucid","")
	oid     = request.POST.get("oid","'")

	print("Stime=%sEtime=%sucid=%soid-%s"%(Stime,Etime,ucid,oid))
	start=200
	return JsonRes(json.dumps(start))



