from django.http import JsonResponse
from django.views import View
import register_webhook

class YookassaPaymentHistoryView(View):
    def get(self, request, *args, **kwargs):
        try:
            # Вызываем функцию для получения истории платежей
            payment_history = register_webhook.payment_webhook()

            # Возвращаем JSON-ответ
            return JsonResponse(payment_history)
        except Exception as e:
            # В случае ошибки возвращаем сообщение об ошибке
            return JsonResponse({"error": str(e)}, status=500)