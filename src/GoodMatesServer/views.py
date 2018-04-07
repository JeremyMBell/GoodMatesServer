from django.core import serializers
from GoodMatesServer.models import User
from django.http import JsonResponse, HttpResponse
import json

def create_user(request):
	first_name = request.POST.get("first_name")
	last_name = request.POST.get("last_name")

	if first_name is not None and last_name is not None:
		user = User(first_name=first_name, last_name=last_name)
		user.save()
		data = serializers.serialize("json", user)
		return JsonResponse(json.loads(data))

	resp = HttpResponse("You did not enter a first name and/or last name")
	resp.status_code = 400
	return resp
	