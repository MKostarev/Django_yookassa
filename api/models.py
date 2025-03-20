from django.db import models

class Payment(models.Model):
    payment_id = models.CharField(max_length=100, unique=True)  # Уникальный ID платежа
    status = models.CharField(max_length=50, blank=True, null=True)  # Статус платежа (необязательное)
    amount_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Сумма (необязательное)
    amount_currency = models.CharField(max_length=3, blank=True, null=True)  # Валюта (необязательное)
    description = models.TextField(blank=True, null=True)  # Описание (необязательное)
    payment_method_type = models.CharField(max_length=50, blank=True, null=True)  # Тип платежа (необязательное)
    payment_method_id = models.CharField(max_length=100, blank=True, null=True)  # ID метода оплаты (необязательное)
    payment_method_title = models.CharField(max_length=100, blank=True, null=True)  # Название метода оплаты (необязательное)
    payment_method_account_number = models.CharField(max_length=50, blank=True, null=True)  # Номер счета (необязательное)
    cps_phone = models.CharField(max_length=20, blank=True, null=True)  # Телефон (необязательное)
    cust_name = models.CharField(max_length=100, blank=True, null=True)  # Имя клиента (необязательное)
    cms_name = models.CharField(max_length=100, blank=True, null=True)  # Название CMS (необязательное)
    cps_email = models.EmailField(blank=True, null=True)  # Email (необязательное)

    def __str__(self):
        return f"Payment {self.payment_id} ({self.status})"

class Payment_model(models.Model):
    payment_id = models.CharField(max_length=100, unique=True)  # Уникальный ID платежа
    status = models.CharField(max_length=50, blank=True, null=True)  # Статус платежа (необязательное)
    amount_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Сумма (необязательное)
    amount_currency = models.CharField(max_length=3, blank=True, null=True)  # Валюта (необязательное)
    description = models.TextField(blank=True, null=True)  # Описание (необязательное)
    payment_method_type = models.CharField(max_length=50, blank=True, null=True)  # Тип платежа (необязательное)
    payment_method_id = models.CharField(max_length=100, blank=True, null=True)  # ID метода оплаты (необязательное)
    payment_method_title = models.CharField(max_length=100, blank=True, null=True)  # Название метода оплаты (необязательное)
    payment_method_account_number = models.CharField(max_length=50, blank=True, null=True)  # Номер счета (необязательное)
    cps_phone = models.CharField(max_length=20, blank=True, null=True)  # Телефон (необязательное)
    cust_name = models.CharField(max_length=100, blank=True, null=True)  # Имя клиента (необязательное)
    cms_name = models.CharField(max_length=100, blank=True, null=True)  # Название CMS (необязательное)
    cps_email = models.EmailField(blank=True, null=True)  # Email (необязательное)

    def __str__(self):
        return f"Payment {self.payment_id} ({self.status})"