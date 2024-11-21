import mercadopago

sdk = mercadopago.SDK("TEST-842210080108555-112009-7bb9f8f2b6c7f8e8f6aaf9e9432dcf97-243287541")

def create_payment_preference():
    preference_data = {
        "items": [
            {
                "title": "Premium Membership",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": 100.00  
            }
        ],
        "back_urls": {
            "success": "http://www.your-site.com/payment/success", 
            "failure": "http://www.your-site.com/payment/failure",
            "pending": "http://www.your-site.com/payment/pending"
        },
        "auto_return": "approved",
    }

    preference_response = sdk.preference().create(preference_data)
    return preference_response["response"]["id"]

