from yookassa import Configuration, Webhook

import config

#Configuration.configure_auth_token("test_emhnq89MvLae72jLpQoHX3He9HoPiatyn4702pmLy0U")
Configuration.configure(config.id_shop, config.api_key)

response = Webhook.add({
    "event": "payment.succeeded",
    "url": "https://priemkassa.local:8443/webhook/",
})
print(response)