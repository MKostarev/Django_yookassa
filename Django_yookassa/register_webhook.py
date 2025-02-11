from yookassa import Configuration, Webhook

import config
import var_dump as var_dump
from yookassa import Payment
Configuration.account_id = config.id_shop
Configuration.secret_key = config.api_key


# Конфигурация
YOOKASSA_SHOP_ID = config.id_shop
YOOKASSA_SECRET_KEY = config.api_key
YOOKASSA_API_URL = config.api_url

cursor = None
data = {
    "limit": 10,                                    # Ограничиваем размер выборки
    "payment_method": "yoo_money",                 # Выбираем только оплату через кошелек
    "created_at.gte": "2020-08-08T00:00:00.000Z",  # Созданы начиная с 2020-08-08
    "created_at.lt": "2025-03-20T00:00:00.000Z"    # И до 2020-10-20
}

while True:
    params = data
    if cursor:
        params['cursor'] = cursor
    try:
        res = Payment.list(params)
        print(" items: " + str(len(res.items)))    # Количество платежей в выборке
        print("cursor: " + str(res.next_cursor))   # Указательна следующую страницу
        var_dump.var_dump(res)

        if not res.next_cursor:
            break
        else:
            cursor = res.next_cursor
    except Exception as e:
        print(" Error: " + str(e))
        break
