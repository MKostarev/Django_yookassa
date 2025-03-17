from django.shortcuts import render

# Create your views here.
from django.db import transaction
from yookassa import Configuration, Payment
import var_dump as var_dump
import pprint
import config
import os
import django

# Настройка Django-окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django_yookassa.settings')
django.setup()

# Конфигурация
Configuration.account_id = config.id_shop
Configuration.secret_key = config.api_key

def fetch_payments(limit=2, created_at_gte="2020-08-08T00:00:00.000Z", created_at_lt="2025-02-20T00:00:00.000Z"):
    # Инициализация параметров запроса
    data = {
        "limit": limit,                    # Ограничиваем размер выборки
        "payment_method": "yoo_money",     # Выбираем только оплату через кошелек
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
            print("Items: " + str(len(res.items)))    # Количество платежей в выборке
            print("Cursor: " + str(res.next_cursor))  # Указатель на следующую страницу

            all_payments.extend(res.items) # Добавляем платежи в общий список

            var_dump.var_dump(res) # Вывод содержимого объекта

            if not res.next_cursor:
                break
            else:
                cursor = res.next_cursor
        except Exception as e:
            print("Error: " + str(e))
            break

    return all_payments  # Возвращаем все полученные платежи


def filter_payments(payments):
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
            "payment_id": payment._PaymentResponse__id,  # Используем атрибуты объекта
            "status": payment._PaymentResponse__status,
            "amount_value": float(payment._PaymentResponse__amount._Amount__value),
            "amount_currency": payment._PaymentResponse__amount._Amount__currency,
            "description": payment._PaymentResponse__description,
            "payment_method_type": payment._PaymentResponse__payment_method._PaymentData__type,
            "payment_method_id": payment._PaymentResponse__payment_method._ResponsePaymentData__id,
            "payment_method_title": payment._PaymentResponse__payment_method._ResponsePaymentData__title,
            "payment_method_account_number": payment._PaymentResponse__payment_method.account_number,
            "cps_phone": payment._PaymentResponse__metadata.get('cps_phone'),
            "cust_name": payment._PaymentResponse__metadata.get('custName'),
            "cms_name": payment._PaymentResponse__metadata.get('cms_name'),
            "cps_email": payment._PaymentResponse__metadata.get('cps_email'),
        })
    return filtered_data





def save_payments_to_db(filtered_payments):
    """
    Сохраняет отфильтрованные данные о платежах в базу данных.
    :param filtered_payments: Список словарей с данными о платежах.
    """
    with transaction.atomic():
        try:
            for payment_data in filtered_payments:
                print(f"Сохраняем: {payment_data}")  # Добавленный лог
                # Создаём или обновляем запись в базе данных
                payment, created = Payment.objects.update_or_create(
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
#filtered_payments = filter_payments(payments_data) # Сохраняем данные в базу
#save_payments_to_db(filtered_payments)# Сохраняем данные в базу
# Выводим отфильтрованные данные
#pprint.pprint(filtered_payments)
