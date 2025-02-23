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


def filter_payments(payments):
    """
    Фильтрует данные о платежах, оставляя только нужные поля.
    :param payments: Список платежей.
    :return: Отфильтрованный список платежей.
    """
    filtered_data = []
    for payment in payments:
        filtered_data.append({
            "payment_id": payment.get("id"),
            "status": payment.get("status"),
            "amount_value": payment.get("amount", {}).get("value"),
            "amount_currency": payment.get("amount", {}).get("currency"),
            "description": payment.get("description"),
            "payment_method_type": payment.get("payment_method", {}).get("type"),
            "payment_method_id": payment.get("payment_method", {}).get("id"),
            "payment_method_title": payment.get("payment_method", {}).get("title"),
            "payment_method_account_number": payment.get("payment_method", {}).get("account_number"),
            "cps_phone": payment.get("metadata", {}).get("cps_phone"),
            "cust_name": payment.get("metadata", {}).get("custName"),
            "cms_name": payment.get("metadata", {}).get("cms_name"),
            "cps_email": payment.get("metadata", {}).get("cps_email"),
        })
    return filtered_data

# Получаем данные от API
payments_data = fetch_payments()

# Фильтруем данные
filtered_payments = filter_payments(payments_data)

# Выводим отфильтрованные данные
import pprint
pprint.pprint(filtered_payments)