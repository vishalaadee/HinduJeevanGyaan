import stripe
from fastapi import HTTPException
import os

stripe.api_key = "sk_test_..."  # Use environment variables in production

def create_checkout_session(amount_rupees: int, user_email: str, appointment_id: int):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "inr",
                    "unit_amount": amount_rupees * 100,
                    "product_data": {"name": "Astrology Service"}
                },
                "quantity": 1
            }],
            mode="payment",
            success_url=f"http://localhost:8000/payment/success?appointment_id={appointment_id}",
            cancel_url="http://localhost:8000/payment/cancel",
            customer_email=user_email
        )
        return session.url
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
