from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .tasks import sendEmailTask
import json
import re


@csrf_exempt
def sendEmails(request):
    received_json_data = json.loads(request.body.decode("utf-8"))
    urls = received_json_data.get("urls")
    email = received_json_data.get("email")
    if len(urls) != 0 and len(re.findall("^\w+@\w+\.\w+$", email)) != 0:
        sendEmailTask.delay(urls=urls, email=email)
    else:
        return HttpResponse("Either mail is invalid or urls are missing")
    return HttpResponse("<html><h1> Mail will be sent asynchronoulsy through celery</h1></html>")
