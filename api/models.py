from django.db import models
from django.contrib.auth.models import User

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
    seminar = models.CharField(max_length=300, blank=True, null=True)  # Описание (необязательное)
    date = models.CharField(max_length=100,blank=True, null=True)  # Описание (необязательное)
    cps_phone = models.CharField(max_length=20, blank=True, null=True)  # Телефон (необязательное)
    cust_name = models.CharField(max_length=100, blank=True, null=True)  # Имя клиента (необязательное)
    cps_email = models.EmailField(blank=True, null=True)  # Email (необязательное)
    cms_name = models.CharField(max_length=100, blank=True, null=True)  # Название CMS (необязательное)
    details_party = models.CharField(max_length=100, blank=True, null=True)  # Метод оплаты

    def __str__(self):
        return f"Payment {self.payment_id} ({self.status})"


class Student(models.Model):
    student_name = models.CharField(max_length=200, blank=True, null=True)  # Имя клиента (необязательное)
    student_phone = models.CharField(max_length=20, blank=True, null=True)  # Телефон (необязательное)
    student_email = models.EmailField(blank=True, null=True)  # Email (необязательное)

    def __str__(self):
        return self.student_name

class Seminar(models.Model):
    seminar_name = models.CharField(max_length=300, blank=True, null=True)  # Название семинара
    description = models.TextField(blank=True, null=True) # Описание семинара

    def __str__(self):
        return self.seminar_name

class Seminar_studet(models.Model):
    seminar = models.ForeignKey(Seminar, on_delete=models.CASCADE)  # Связь с семинаром
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Связь со студентом

    def __str__(self):
        return f"{self.student.student_name} -> {self.seminar.seminar_name}"


class SeminarRegistration(models.Model):
    seminar_name = models.CharField(max_length=500, verbose_name="Название семинара", null=True, blank=True)
    student_name = models.CharField(max_length=255, verbose_name="ФИО студента", null=True, blank=True)
    student_email = models.EmailField(verbose_name="Email студента", null=True, blank=True)
    student_phone = models.CharField(max_length=20, verbose_name="Телефон студента", null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации", null=True, blank=True)

    class Meta:
        verbose_name = "Регистрация на семинар"
        verbose_name_plural = "Регистрации на семинары"
        ordering = ['-registration_date']

    def __str__(self):
        return f"{self.student_name} - {self.seminar_name}"