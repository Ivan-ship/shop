from uuid import uuid4
from yookassa import Payment, Configuration
from config.config import configuration

Configuration.account_id = configuration.YOOKASSA_SHOP_ID
Configuration.secret_key = configuration.YOOKASSA_SECRET_KEY


async def create_payment(
    amount: str,
    description: str,
    prod_id: int,
    telegram_id: int
):
    payment = Payment.create(
        {
            "amount": {
                "value": amount,
                "currency": "RUB",

            },
            "confirmation": {
                "type": "redirect",
                "return_url": configuration.RETURN_URL
            },
            "capture": True,
            "description": description,
            "metadata": {
                "prod_id": prod_id,
                "telegram_id": telegram_id
            }
        },
        uuid4()
    )
    return payment