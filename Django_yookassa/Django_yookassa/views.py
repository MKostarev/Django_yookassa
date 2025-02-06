import json
from django.http import HttpResponse, HttpResponseBadRequest
from yookassa.domain.notification import WebhookNotification

def payment_webhook(request):
    # Убедимся, что это POST-запрос
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method")

    try:
        # Получаем JSON из тела запроса
        event_json = json.loads(request.body)

        # Создаём объект WebhookNotification
        notification_object = WebhookNotification(event_json)

        # Доступ к типу события и объекту платежа
        event_type = notification_object.event
        payment_object = notification_object.object

        if event_type == "payment.succeeded":
            print(f"Платёж {payment_object.id} успешно завершён.")
        elif event_type == "payment.waiting_for_capture":
            print(f"Платёж {payment_object.id} ожидает подтверждения.")
        else:
            print(f"Неизвестный тип события: {event_type}")

        return HttpResponse(status=200)

    except Exception as e:
        print(f"Ошибка обработки webhook: {e}")
        return HttpResponseBadRequest("Invalid webhook data")
