from django.db import models

class Payment(models.Model):
    payment_id = models.CharField(max_length=100, unique=True)  # Уникальный ID платежа
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Сумма платежа
    status = models.CharField(max_length=50)  # Статус платежа (например, "succeeded", "pending", "canceled")
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания платежа
    description = models.TextField(blank=True, null=True)  # Описание платежа

    def __str__(self):
        return f"Payment {self.payment_id} ({self.status})"