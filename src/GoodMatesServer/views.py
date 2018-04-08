from django.core import serializers
from GoodMatesServer.models import *
from django.http import JsonResponse, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
DATETIME_FORMAT = "%m/%d/%Y %I:%M:%S %p"
def jsonize(obj):
	if isinstance(obj, list):
		return serializers.serialize("json", obj)
	else:
		return jsonize([obj,])

def parse_request(request):
	return request.POST
	if len(request.POST) == 0:
		return {}
	elif len(request.POST) == 1:
		return json.loads(request.POST.keys()[0])
	else:
		to_return = []
		for key in request.POST:
			to_return.append(json.loads(key))
		return to_return

@csrf_exempt
def create_user(request):
	request = parse_request(request)
	first_name = request.get("first_name")
	last_name = request.get("last_name")
	uid = request.get("uid")

	if first_name is not None and last_name is not None:
		user = User(first_name=first_name, last_name=last_name, uid=uid, registered=datetime.now())
		user.save()
		data = jsonize(user)
		return JsonResponse(json.loads(data), safe=False)
	else:
		resp = HttpResponse("You did not enter a first name and/or last name")
		resp.status_code = 400
		return resp


@csrf_exempt
def create_group(request):
	request = parse_request(request)
	try:
		code = request.get("code")
		userid = request.get("uid")
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
		if code is not None and code.isalnum() and len(code) == 8:
			group = Group(uid=code, registered=datetime.now())
			group.save()
			data = jsonize(group)
			user.group = group
			user.save()
			return JsonResponse(json.loads(data), safe=False)
		else:
			resp = HttpResponse("Invalid group code.")
			resp.status_code = 400
			return resp


@csrf_exempt
def join_group(request):
	request = parse_request(request)
	try:
		code = request.get("code")
		userid = request.get("uid")
		user = User.objects.get(uid=userid)
		group = Group.objects.get(uid=code)
	except:
		resp = HttpResponse("Group does not exist")
		resp.status_code = 400
		return resp

	user.group = group
	user.save()
	data = jsonize(user)
	return JsonResponse(json.loads(data), safe=False)


@csrf_exempt
def book_laundry(request):
	request = parse_request(request)
	try:
		code = request.get("code")
		userid = request.get("uid")
		user = User.objects.get(uid=userid)
		group = Group.objects.get(uid=code)
		start = datetime.strptime(request.get("start_time"), DATETIME_FORMAT)
		stop = datetime.strptime(request.get("end_time"), DATETIME_FORMAT)
	except:
		resp = HttpResponse("User/Group does not exist")
		resp.status_code = 400
		return resp

	laundry = Laundry(start_time=start, end_time=stop, user=userid, group=code)
	laundry.save()
	data = jsonize(laundry)
	return JsonResponse(json.loads(data), safe=False)


@csrf_exempt
def book_shower(request):
	request = parse_request(request)
	try:
		code = request.get("code")
		userid = request.get("uid")
		user = User.objects.get(uid=userid)
		group = Group.objects.get(uid=code)
		start = datetime.strptime(request.get("start_time"), DATETIME_FORMAT)
		stop = datetime.strptime(request.get("end_time"), DATETIME_FORMAT)
	except:
		resp = HttpResponse("User/Group does not exist")
		resp.status_code = 400
		return resp

	shower = Shower(start_time=start, end_time=stop, user=userid, group=code)
	shower.save()
	data = jsonize(shower)
	return JsonResponse(json.loads(data), safe=False)


@csrf_exempt
def note_payment(request):
	request = parse_request(request)
	try:
		creditor = request.get("creditor")
		debtor = request.get("debtor")
		user = User.objects.get(uid=creditor)
		user = User.objects.get(uid=debtor)
		due = request.get("time_due")
		amount = request.get("amount")
	except:
		resp = HttpResponse("User does not exist")
		resp.status_code = 400
		return resp

	payment = Payment(creditor=creditor, debtor=debtor, amount=amount, time_due=due, paid=False)
	payment.save()
	data = jsonize(payment)
	return JsonResponse(json.loads(data), safe=False)