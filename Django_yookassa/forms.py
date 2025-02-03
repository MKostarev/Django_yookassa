from yookassa import Payment

payment = Payment.create({
    "amount": {
        "value": "100.00",  # Сумма платежа
        "currency": "RUB"   # Валюта
    },
    "payment_method_data": {
        "type": "bank_card"  # Тип платежа (например, банковская карта)
    },
    "confirmation": {
        "type": "redirect",  # Перенаправление пользователя на страницу оплаты
        "return_url": "https://example.com/success"  # URL, куда вернётся пользователь после оплаты
    },
    "description": "Оплата товара №1"
})

print(f"Создан платёж: {payment.id}")
print(f"Ссылка для оплаты: {payment.confirmation.confirmation_url}")