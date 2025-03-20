from django.shortcuts import render

# Create your views here.
#from api.models import Payment_model
from django.db import transaction
from yookassa import Configuration, Payment

import var_dump as var_dump
import pprint
import config
import os
import django

from api.models import Payment_model

#Настройка Django-окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django_yookassa.settings')
django.setup()

# Конфигурация
Configuration.account_id = config.id_shop
Configuration.secret_key = config.api_key

def fetch_payments(limit=100, created_at_gte="2025-02-15T00:00:00.000Z", created_at_lt="2025-02-20T00:00:00.000Z"):
    print("Собираем платежи")
    # Инициализация параметров запроса
    data = {
        "limit": limit,                    # Ограничиваем размер выборки
        #"payment_method": "yoo_money",     # Выбираем только оплату через кошелек
        "created_at.gte": created_at_gte,  # Созданы начиная с 2020-08-08
        "created_at.lt": created_at_lt     # И до 2025-03-20
    }
    #Инициализация переменных
    cursor = None
    all_payments = []  # Список для хранения всех платежей

    while True:
        params = data
        if cursor:
            params['cursor'] = cursor

        try:
            res = Payment.list(params)
            print("Количество платежей: " + str(len(res.items)))    # Количество платежей в выборке
            print("Cursor: " + str(res.next_cursor))  # Указатель на следующую страницу

            all_payments.extend(res.items) # Добавляем платежи в общий список

            #var_dump.var_dump(res) # Вывод содержимого объекта

            if not res.next_cursor:
                break
            else:
                cursor = res.next_cursor
        except Exception as e:
            print("Error: " + str(e))
            break
    print(all_payments[0])
    return all_payments  # Возвращаем все полученные платежи


def filter_payments(payments):
    print("Фильтруем платежи")
    #if not filtered_payments:
        #print("Отфильтрованные платежи пустые!")
    """
    Фильтрует данные о платежах, оставляя только нужные поля.
    :param payments: Список объектов PaymentResponse.
    :return: Отфильтрованный список платежей.
    """
    filtered_data = []
    for payment in payments:
        filtered_data.append({
            "payment_id": payment._PaymentResponse__id,  # Уникальный идентификатор платежа
            "status": payment._PaymentResponse__status,  # Статус платежа (успешно/отклонено/ожидает)
            "amount_value": float(payment._PaymentResponse__amount._Amount__value),  # Сумма платежа в числовом формате
            "amount_currency": payment._PaymentResponse__amount._Amount__currency,  # Валюта платежа (USD, RUB и т.д.)
            "description": payment._PaymentResponse__description,  # Описание платежа
            #"payment_method_type": payment._PaymentResponse__payment_method._PaymentData__type, # Тип платежного метода (кредитная карта, PayPal и т.д.)
            #"payment_method_id": payment._PaymentResponse__payment_method._ResponsePaymentData__id, # Идентификатор платежного метода
            #"payment_method_title": payment._PaymentResponse__payment_method._ResponsePaymentData__title, # Название платежного метода
            #"payment_method_account_number": payment._PaymentResponse__payment_method.account_number, # Номер счета/карты для платежного метода
            "cps_phone": payment._PaymentResponse__metadata.get('cps_phone'),  # Телефон клиента
            "cust_name": payment._PaymentResponse__metadata.get('custName'),  # Имя клиента
            "cms_name": payment._PaymentResponse__metadata.get('cms_name'),  # Название используемой CMS
            "cps_email": payment._PaymentResponse__metadata.get('cps_email'),  # Email клиента
        })
    print(filtered_data)
    print(filtered_data[0])
    return filtered_data





def save_payments_to_db(filtered_payments):
    """
    Сохраняет отфильтрованные данные о платежах в базу данных.
    :param filtered_payments: Список словарей с данными о платежах.
    """
    with transaction.atomic():
        try:
            for payment_data in filtered_payments:
                print(f"Сохраняем платежи")  # Добавленный лог
                # Создаём или обновляем запись в базе данных
                payment, created = Payment_model.objects.update_or_create(
                    payment_id=payment_data.get("payment_id"),
                    defaults={
                        "status": payment_data.get("status"),
                        "amount_value": payment_data.get("amount_value"),
                        "amount_currency": payment_data.get("amount_currency"),
                        "description": payment_data.get("description"),
                        "payment_method_type": payment_data.get("payment_method_type"),
                        "payment_method_id": payment_data.get("payment_method_id"),
                        "payment_method_title": payment_data.get("payment_method_title"),
                        "payment_method_account_number": payment_data.get("payment_method_account_number"),
                        "cps_phone": payment_data.get("cps_phone"),
                        "cust_name": payment_data.get("cust_name"),
                        "cms_name": payment_data.get("cms_name"),
                        "cps_email": payment_data.get("cps_email"),
                    }
                )
                if created:
                    print(f"Создан новый платеж: {payment.payment_id}")
                else:
                    print(f"Обновлено: {payment.payment_id}")
        except Exception as e:
            print(f"Ошибка при сохранении платежа: {str(e)}")


# Получаем данные от API
payments_data = fetch_payments()

# Фильтруем данные
filtered_payments = filter_payments(payments_data) #Фильтруем данные в базе
save_payments_to_db(filtered_payments)# Сохраняем данные в базу
# Выводим отфильтрованные данные
#pprint.pprint(filtered_payments)
