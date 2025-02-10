from yookassa import Configuration, Webhook

import config

Configuration.configure(config.api_key)

response = Webhook.add({
    "event": "payment.succeeded",
    "url": "https://priemkassa.local:8443/webhook/",
})


