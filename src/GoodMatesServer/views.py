from django.core import serializers
from GoodMatesServer.models import User
from django.http import JsonResponse, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
import datetime

def jsonize(obj):
	if isinstance(obj, list):
		return serializers.serialize("json", obj, safe=False)
	else:
		return jsonize([obj,])


@csrf_exempt
def create_user(request):
	try:
		first_name = request.POST.get("first_name")
		last_name = request.POST.get("last_name")
		uid = request.POST.get("uid")
	except:
		resp = HttpResponse("Bad create_user request")
		resp.status_code = 400
		return resp

	if first_name is not None and last_name is not None:
		user = User(first_name=first_name, last_name=last_name, uid=uid, registered=datetime.now())
		user.save()
		data = jsonize(user)
		return JsonResponse(json.loads(data))
	else:
		resp = HttpResponse("You did not enter a first name and/or last name")
		resp.status_code = 400
		return resp


@csrf_exempt
def create_group(request):
	try:
		code = request.POST.get("code")
		userid = request.POST.get("uid")
		user = User.objects.get(uid=userid)
	except:
		resp = HttpResponse("Bad create_group request")
		resp.status_code = 400
		return resp

	try:
		group = Group.objects.get(uid=code)
		resp = HttpResponse("Group already exists")
		resp.status_code = 400
		return resp
	except:
		if code is not None and isalnum(code) and len(code) == 8:
			group = Group(uid=code, registered=datetime.now())
			group.save()
			data = jsonize(group)
			user.group = code
			user.save()
			return JsonResponse(json.loads(data))
		else:
			resp = HttpResponse("Invalid group code.")
			resp.status_code = 400
			return resp


@csrf_exempt
def join_group(request):
	try:
		code = request.POST.get("code")
		userid = request.POST.get("uid")
		user = User.objects.get(uid=userid)
		group = Group.objects.get(uid=code)
	except:
		resp = HttpResponse("Group does not exist")
		resp.status_code = 400
		return resp

	user.group = code
	user.save()
	data = jsonize(user)
	return JsonResponse(json.loads(data))