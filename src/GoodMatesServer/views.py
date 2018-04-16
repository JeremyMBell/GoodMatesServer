from django.core import serializers
from GoodMatesServer.models import *
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

DATETIME_FORMAT = "%m/%d/%Y %I:%M %p"
STRFTIME_FORMAT = "%I:%M %p"

def jsonize(obj):
	if isinstance(obj, list):
		return serializers.serialize("json", obj)
	else:
		return jsonize([obj,])

def parse_request(request):
	return request.POST

def overlapping_times(start_time, end_time, group, query_dict):
	in_range = lambda t: Q(start_time__lte=t) & Q(end_time__gte=t)
	return query_dict.filter(in_range(start_time) | in_range(end_time), Q(group=group))

@csrf_exempt
def create_user(request):
	request = parse_request(request)
	first_name = request.get("first_name")
	last_name = request.get("last_name")
	uid = request.get("uid")
	phone = request.get("phone")

	try:
		phone = int(phone)
	except:
		resp = HttpResponse("Invalid phone")
		resp.status_code = 400
		return resp

	if first_name is not None and last_name is not None:
		user = User(first_name=first_name, last_name=last_name, uid=uid, registered=datetime.now(), phone=phone)
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


	laundry = Laundry(start_time=start, end_time=stop, user=user, group=group)
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
		start_time = datetime.strptime(request.get("start_time"), DATETIME_FORMAT)
		end_time = datetime.strptime(request.get("end_time"), DATETIME_FORMAT)
		overlapping_showers = overlapping_times(start_time, end_time, group, Shower.objects)
		if (len(overlapping_showers) > 0):
			resp_str = "Your shower time overlaps with "
			shower_strs = []
			for shower in overlapping_showers:
				user = shower.user
				shower_strs.append(shower.user.first_name + " " + shower.user.last_name + "'s shower at " + shower.start_time.strftime(STRFTIME_FORMAT) + "-" + shower.end_time.strftime(STRFTIME_FORMAT))
			
			last_shower = shower_strs.pop()
			if len(shower_strs) > 1:
				resp_str += ", ".join(shower_strs) + ", and " + last_shower
			else:
				resp_str += last_shower
			resp = JsonResponse([{'error': resp_str}], safe=False)
			resp.status_code = 406
			return resp
	except:
		resp = HttpResponse("User/Group does not exist")
		resp.status_code = 400
		return resp

	shower = Shower(start_time=start_time, end_time=end_time, user=user, group=group)
	shower.save()
	data = jsonize(shower)
	return JsonResponse(json.loads(data), safe=False)


@csrf_exempt
def note_guests(request):
	request = parse_request(request)
	try:
		code = request.get("code")
		userid = request.get("uid")
		user = User.objects.get(uid=userid)
		group = Group.objects.get(uid=code)
		start = datetime.strptime(request.get("start_time"), DATETIME_FORMAT)
		stop = datetime.strptime(request.get("end_time"), DATETIME_FORMAT)
		num_guests = request.get("num_guests")
		needs_privacy = request.get("needs_privacy")
	except:
		resp = HttpResponse("User/Group does not exist")
		resp.status_code = 400
		return resp

	guests = Guests(user=user, group=group, start_time=start, end_time=stop, num_guests=num_guests, needs_privacy=needs_privacy)
	guests.save()
	data = jsonize(guests)
	return JsonResponse(json.loads(data), safe=False)


@csrf_exempt
def note_payment(request):
	request = parse_request(request)
	try:
		creditor_uid = request.get("creditor")
		debtor_uid = request.get("debtor")
		creditor = User.objects.get(uid=creditor_uid)
		debtor = User.objects.get(uid=debtor_uid)
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


@csrf_exempt
def note_chore(request):
	request = parse_request(request)
	try:
		code = request.get("code")
		userid = request.get("uid")
		user = User.objects.get(uid=userid)
		group = Group.objects.get(uid=code)
		due = datetime.strptime(request.get("time_due"), DATETIME_FORMAT)
		notes = request.get("notes")
	except:
		resp = HttpResponse("User/Group does not exist")
		resp.status_code = 400
		return resp

	chore = Chore(user=user, group=group, time_due=due, notes=notes)
	chore.save()
	data = jsonize(chore)
	return JsonResponse(json.loads(data), safe=False)


@csrf_exempt
def note_plan(request):
	request = parse_request(request)
	try:
		code = request.get("code")
		group = Group.objects.get(uid=code)
		start = datetime.strptime(request.get("start_time"), DATETIME_FORMAT)
		stop = datetime.strptime(request.get("end_time"), DATETIME_FORMAT)
		notes = request.get("notes")
	except:
		resp = HttpResponse("User/Group does not exist")
		resp.status_code = 400
		return resp

	plan = Plan(group=group, start_time=start, end_time=stop, notes=notes)
	plan.save()
	data = jsonize(plan)
	return JsonResponse(json.loads(data), safe=False)



@csrf_exempt
def get_user(request):
	try:
		userid = request.GET.get("uid")
		user = User.objects.get(uid=userid)
	except:
		resp = HttpResponse("User does not exist")
		resp.status_code = 400
		return resp

	return JsonResponse(json.loads(jsonize(user)), safe=False)


@csrf_exempt
def get_group(request):
	try:
		uid = request.GET.get("code")
		group = Group.objects.get(uid=uid)
	except:
		resp = HttpResponse("Group does not exist")
		resp.status_code = 400
		return resp
	data = json.loads(jsonize(group))
	data[0]["users"] = json.loads(jsonize(list(group.user_set.all())))
	return JsonResponse(data, safe=False)


@csrf_exempt
def get_laundry(request):
	try:
		group = request.GET.get("code")
		laundries = Group.objects.get(uid=group).laundry_set.all()
	except:
		resp = HttpResponse("Group does not exist")
		resp.status_code = 400
		return resp

	return JsonResponse(json.loads(jsonize(laundries)), safe=False)


@csrf_exempt
def get_shower(request):
	try:
		group = request.GET.get("code")
		showers = Group.objects.get(uid=group).shower_set.all()
	except:
		resp = HttpResponse("Group does not exist")
		resp.status_code = 400
		return resp

	return JsonResponse(json.loads(jsonize(showers)), safe=False)


@csrf_exempt
def get_payment(request):
	try:
		userid = request.GET.get("uid")
		payments = User.objects.get(uid=userid).payment_set.all()
	except:
		resp = HttpResponse("User does not exist")
		resp.status_code = 400
		return resp

	return JsonResponse(json.loads(jsonize(payments)), safe=False)


@csrf_exempt
def get_guests(request):
	try:
		group = request.GET.get("code")
		guests = Group.objects.get(uid=group).guests_set.all()
	except:
		resp = HttpResponse("Group does not exist")
		resp.status_code = 400
		return resp

	return JsonResponse(json.loads(jsonize(guests)), safe=False)


@csrf_exempt
def get_chore(request):
	try:
		group = request.GET.get("code")
		chores = Group.objects.get(uid=group).chore_set.all()
	except:
		resp = HttpResponse("Group does not exist")
		resp.status_code = 400
		return resp

	return JsonResponse(json.loads(jsonize(chores)), safe=False)


@csrf_exempt
def get_plan(request):
	try:
		group = request.GET.get("code")
		plans = Group.objects.get(uid=group).plan_set.all()
	except:
		resp = HttpResponse("Group does not exist")
		resp.status_code = 400
		return resp

	return JsonResponse(json.loads(jsonize(plans)), safe=False)
