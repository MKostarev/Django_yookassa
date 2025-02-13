from yookassa import Configuration, Payment
import config
import var_dump as var_dump

# Конфигурация
Configuration.account_id = config.id_shop
Configuration.secret_key = config.api_key

def fetch_payments(limit=10, created_at_gte="2020-08-08T00:00:00.000Z", created_at_lt="2025-03-20T00:00:00.000Z"):
    # Параметры запроса
    data = {
        "limit": limit,                                    # Ограничиваем размер выборки
        "payment_method": "yoo_money",                 # Выбираем только оплату через кошелек
        "created_at.gte": created_at_gte,  # Созданы начиная с 2020-08-08
        "created_at.lt": created_at_lt    # И до 2025-03-20
    }

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


    return  # Возвращаем все полученные платежи

fetch_payments()

def filter_payments(payments, filters):
    """
    Фильтрует список платежей по заданным параметрам и оставляет только нужные поля.

    :param payments: Список платежей, полученных из API.
    :param filters: Словарь с параметрами фильтрации.
    :return: Отфильтрованный список платежей с нужными полями.
    """
    filtered_payments = []

    for payment in payments:
        match = True  # Предполагаем, что платеж соответствует всем условиям

        # Проверяем каждый параметр фильтрации
        for key, value in filters.items():
            # Если параметр отсутствует в платеже или не совпадает, пропускаем платеж
            if not hasattr(payment, key) or getattr(payment, key) != value:
                match = False
                break

        # Если все условия выполнены, добавляем платеж в отфильтрованный список
        if match:
            # Создаем словарь с нужными полями
            filtered_payment = {
                "payment_id": payment.id,
                "status": payment.status,
                "amount_value": payment.amount.value,
                "amount_currency": payment.amount.currency,
                "description": payment.description,
                "payment_method_type": payment.payment_method.type if hasattr(payment, 'payment_method') else None,
                "payment_method_id": payment.payment_method.id if hasattr(payment, 'payment_method') else None,
                "payment_method_title": payment.payment_method.title if hasattr(payment, 'payment_method') else None,
                "payment_method_account_number": payment.payment_method.account_number if hasattr(payment, 'payment_method') else None,
                "cps_phone": payment.metadata.get('cps_phone') if hasattr(payment, 'metadata') else None,
                "cust_name": payment.metadata.get('cust_name') if hasattr(payment, 'metadata') else None,
                "cms_name": payment.metadata.get('cms_name') if hasattr(payment, 'metadata') else None,
                "cps_email": payment.metadata.get('cps_email') if hasattr(payment, 'metadata') else None,
            }
            filtered_payments.append(filtered_payment)

    return filtered_payments

