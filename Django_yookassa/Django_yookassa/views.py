import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Exempt this view from CSRF protection
def payment_webhook(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method.")

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON payload.")

    #http://127.0.0.1:4040/webhook

    # Perform different actions based on the event type
    #event_type = data.get("event_type")

    #if event_type == "payment_success":
    #    handle_payment_success(data)
    #elif event_type == "payment_failure":
    #    handle_payment_failure(data)
    #else:
        #return HttpResponseBadRequest("Unhandled event type.")

    # Acknowledge receipt of the webhook
    return JsonResponse({"status": "success"})