import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse

@csrf_exempt  # Exempt this view from CSRF protection
def payment_webhook(request):
    return HttpResponse("Привет, это просто текст!", content_type="text/plain; charset=utf-8")
