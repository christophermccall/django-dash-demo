import stripe
import os
import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dashboard_demo.settings")
django.setup()

try:
    stripe.api_key = settings.STRIPE_SECRET_KEY
    config = stripe.billing_portal.Configuration.create(
        features={
            "invoice_history": {"enabled": True},
            "payment_method_update": {"enabled": True},
            "subscription_cancel": {"enabled": True, "mode": "immediately"},
            "subscription_update": {
                "enabled": True,
                "default_allowed_updates": ["price"],
                "proration_behavior": "create_prorations",
                "products":[
                    {
                        "product": "prod_RrcrldzFZmVdXa",
                        "prices": ["price_1Qxtc6JNY05FwokpJCjk5rXe"]
                    }
                ]
            },
            "customer_update": {
                "enabled": True,
                "allowed_updates": ["email", "tax_id", "address", "phone"],
            }
        }
    )
    print(f"Billing Portal configuration created successfully! ID: {config.id}")

except stripe.error.StripeError as e:
    print(f"Stripe API error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

