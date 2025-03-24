from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import get_messages
from django.db.models import Count
from django.db.models.functions import TruncDate
from django_ratelimit.decorators import ratelimit
from django.http import JsonResponse
from .models import UserActivity, Profile
from django.views.decorators.csrf import csrf_exempt
import stripe
import logging
from .models import Subscription
from django.conf import settings
from django.core.cache import cache
import datetime
from django.utils import timezone
from django.utils.timezone import make_aware

stripe.api_key = settings.STRIPE_SECRET_KEY

PRODUCT_PRICES = {
    'iphone': 'price_1R3iqWJNY05FwokpDNKkdIDq',
    'airpods': 'price_1R3isCJNY05FwokpqWRhnTZj',
    'ps5': 'price_1R3it0JNY05FwokpJ0N1d496',
}

logger = logging.getLogger(__name__)


def rate_limit(request, key_prefix="rate_limit", limit=10000, timeout=60):
    client_ip = request.META.get("REMOTE_ADDR")
    user_id = request.user.id

    key = f"{key_prefix}:{user_id}"

    request_count = cache.get(key, 0)

    if request_count >= limit:
        return JsonResponse({"error": "Too many requests"}, status=429)
    cache.set(key, request_count + 1, timeout=timeout)

    return None 

# Dashboard - Requires Login
@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'dashboard/index.html')

@login_required(login_url='login')
def overview(request):
    return render(request, 'dashboard/overview.html')

@login_required(login_url='login')
def products(request):
    return render(request, 'dashboard/products.html')

@login_required(login_url='login')
def activities(request):
    return render(request, 'dashboard/activities.html')

@login_required(login_url='login')
def logs(request):
    return render(request, 'dashboard/logs.html')

@login_required(login_url='login')
def payouts(request):
    return render(request, 'dashboard/payouts.html')

@login_required(login_url='login')
def profiles(request):
    return render(request, 'dashboard/profiles.html')

@login_required(login_url='login')
def user_settings(request):
    return render(request, 'dashboard/user_settings.html')

def index(request):
    return render(request, 'index.html')

def success_view(request):
    return render(request, 'success.html')

def cancel_view(request):
    return render(request, 'cancel.html')

@login_required(login_url='login')
def create_checkout_session(request):
    return render(request, 'dashboard/checkout.html')

# Signup Page
def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            messages.error(request, "Your password and confirm password do not match!")
            return redirect('signup')
        
        if User.objects.filter(username=uname).exists():
            messages.warning(request, "Username already taken. Try another one.")
            return redirect('signup')

        # User creation (Corrected indentation)
        my_user = User.objects.create_user(username=uname, email=email, password=pass1)
        my_user.save()

        # Logging for console
        logger.info(f"New user {uname} registered with email {email}.")

        # Logging for database (Use `my_user`, not `request.user`)
        UserActivity.objects.create(
            user=my_user,
            action="account creation",
            ip_address=request.META.get('REMOTE_ADDR'),
            page=request.path
        )

        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, 'signup.html')

# Login Page
def LoginPage(request):

    storage = get_messages(request)  # Consume messages so they don't persist
    for _ in storage:
        pass  # This will clear any existing messages

    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)

        if user is not None:
            login(request, user)
            logger.info(f"User {username} logged in")

            # Logging user activity
            UserActivity.objects.create(
                user=user,  # Use authenticated `user`, not `request.user`
                action="logged in",
                ip_address=request.META.get('REMOTE_ADDR'),
                page=request.path
            )

            messages.success(request, "You have successfully logged in.")
            return redirect('dashboard')

        else:
            logger.warning(f"Failed login attempt for username {username}")
            messages.error(request, "Invalid username or password!")
            return redirect('login')  

    return render(request, 'login.html')

# Logout Page
def LogoutPage(request):
    if request.user.is_authenticated:  # Check if user is logged in
        username = request.user.username

        # Logging user activity before logout
        UserActivity.objects.create(
            user=request.user,
            action="logged out",
            ip_address=request.META.get('REMOTE_ADDR'),
            page=request.path
        )

        logout(request)  
        logger.info(f"User {username} logged out.")

        # Consume messages to prevent them from persisting
        storage = get_messages(request)
        for _ in storage:
            pass  # Access messages to clear them

        messages.info(request, "You have been logged out successfully.")

    return redirect('login')

# Get login counts per day
# this decorator is used to limit the amount of requets per user based on their ip
def get_logins_per_day(request):
    user = request.user
    # Rate limiting
    rate_limit_response = rate_limit(request, key_prefix="logins", limit=100, timeout=60)
    if rate_limit_response:
        return rate_limit_response

    # Check subscription
    try:
        sub = Subscription.objects.filter(user=user).first()
        # Ensure the subscription is active
        if sub.status != "active":
            return JsonResponse({"subscription_required": True, "message": "Subscription required"})

        # Enforce API usage limit (max 10 requests)
        if sub.tracker_request_count >= 50:
            return JsonResponse({
                "subscription_required": True,
                "message": "API request limit reached. Upgrade your plan."
            })

        # Increment API request count
        sub.tracker_request_count += 1
        sub.save()

    except Subscription.DoesNotExist:
        return JsonResponse({"subscription_required": True, "message": "No subscription found"})

    # Fetch login data
    try:
        login_data = (
            UserActivity.objects
            .filter(action='logged in')
            .annotate(login_date=TruncDate('timestamp'))
            .values('login_date')
            .annotate(login_count=Count('id'))
            .order_by('login_date')
        )

        logger.info(f"Login data: {login_data}")

        result = [
            {
                "login_date": entry['login_date'].strftime('%Y-%m-%d'),
                "login_count": entry['login_count']
            }
            for entry in login_data
        ]

        return JsonResponse({"subscription_required": False, "data": result}, safe=False)

    except Exception as e:
        logger.error(f"Error in get_logins_per_day view: {str(e)}")
        return JsonResponse({"error": "An error occurred while processing your request. Please try again."}, status=500)




#checkout session

@login_required(login_url='login')
def create_sub_checkout_session(request):
    user = request.user

    # Check if user already has an active subscription
    existing_subscription = Subscription.objects.filter(user=user).first()

    if existing_subscription and existing_subscription.status == "active":
        return redirect("/dashboard/")  # Redirect if already subscribed

    # Create a Stripe Checkout Session
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {"price": "price_1R4kIqJNY05FwokpbkMS6YDo", "quantity": 1},
            {"price": "price_1R4kO2JNY05FwokpjkT0UZFM"},
        ],
        mode="subscription",
        success_url="http://127.0.0.1:8000/success/",
        cancel_url="http://127.0.0.1:8000/cancel/",
        customer_email=user.email,  # Prefill the user's email
)

# Store both price IDs
    Subscription.objects.create(
        user=user,
        stripe_checkout_session_id=checkout_session.id,
        stripe_price_ids=["price_1R4kIqJNY05FwokpbkMS6YDo", "price_1R4kO2JNY05FwokpjkT0UZFM"],  # Store as a list
        status="pending",
    )

    return redirect(checkout_session.url)





#webhook

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return JsonResponse({"error": "Invalid payload"}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({"error": "Invalid signature"}, status=400)

    # Initialized IDs to Avoid "Referenced Before Assignment" Error
    customer_id = None
    subscription_id = None
    checkout_session_id = None

    # When a user completes checkout (New Subscription)
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_id = session.get("customer")
        subscription_id = session.get("subscription")
        checkout_session_id = session.get("id")

        if not customer_id or not subscription_id:
            return JsonResponse({"error": "Missing customer or subscription ID"}, status=400)

        subscription = Subscription.objects.filter(stripe_checkout_session_id=checkout_session_id).first()
        
        if not subscription:
            return JsonResponse({"error": "Subscription not found"}, status=400)

        try:
            # Retrieve full subscription details
            stripe_subscription = stripe.Subscription.retrieve(subscription_id)
            price_ids = [item["price"]["id"] for item in stripe_subscription["items"]["data"]]
            subscription_item_ids = [item["id"] for item in stripe_subscription["items"]["data"]]

            # Convert UNIX timestamp to Django datetime
            current_period_end_unix = stripe_subscription["current_period_end"]
            current_period_end_dt = timezone.make_aware(datetime.datetime.utcfromtimestamp(current_period_end_unix))

            # Update subscription details
            subscription.stripe_customer_id = customer_id
            subscription.stripe_subscription_id = subscription_id
            subscription.stripe_price_ids = price_ids
            subscription.stripe_subscription_item_ids = subscription_item_ids
            subscription.status = stripe_subscription["status"]
            subscription.current_period_end = current_period_end_dt
            subscription.save()

            logger.info(f"Subscription updated: {subscription}")

        except Exception as e:
            logger.error(f"Error updating subscription: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    # When a subscription is updated (plan upgrade/downgrade)
    elif event["type"] == "customer.subscription.updated":
        subscription_data = event["data"]["object"]
        subscription_id = subscription_data["id"]

        try:
            # Find subscription in database
            subscription = Subscription.objects.get(stripe_subscription_id=subscription_id)

            # Get updated status
            status = subscription_data["status"]

            # Handle missing price information safely
            if "items" in subscription_data and subscription_data["items"]["data"]:
                price_id = subscription_data["items"]["data"][0].get("price", {}).get("id", None)
            else:
                price_id = None  # Handle missing price ID safely

            # Convert UNIX timestamp to Django datetime
            current_period_end_unix = subscription_data["current_period_end"]
            current_period_end_dt = make_aware(datetime.datetime.utcfromtimestamp(current_period_end_unix))

            # Update subscription details
            subscription.stripe_price_id = price_id
            subscription.status = status
            subscription.current_period_end = current_period_end_dt
            subscription.save()

            logger.info(f"Subscription updated (upgrade/downgrade): {subscription}")

        except Subscription.DoesNotExist:
            logger.error(f"Subscription {subscription_id} not found for update.")
            return JsonResponse({"error": "Subscription not found"}, status=400)
            

    # When a subscription is canceled
    elif event["type"] == "customer.subscription.deleted":
        subscription_data = event["data"]["object"]
        subscription_id = subscription_data["id"]

        try:
            # Find the subscription
            subscription = Subscription.objects.get(stripe_subscription_id=subscription_id)

            # Mark it as canceled
            subscription.status = "canceled"
            subscription.save()

            logger.info(f"Subscription canceled: {subscription}")

        except Subscription.DoesNotExist:
            logger.error(f"Subscription {subscription_id} not found for cancellation.")
            return JsonResponse({"error": "Subscription not found"}, status=400)

    return JsonResponse({"status": "success"}, status=200)






# User Profile
@login_required
def profiles(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        company_name = request.POST.get('company_name')
        organization_type = request.POST.get('organization_type')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        if full_name and email:
            user.email = email
            profile.full_name = full_name
            profile.company_name = company_name
            profile.organization_type = organization_type
            profile.phone_number = phone_number
            profile.address = address

            user.save()
            profile.save()
            
            messages.success(request, "Profile updated successfully!")

            return redirect('profiles')
        else:
            messages.error(request, "Full Name and Email are required fields.")

    return render(request, 'dashboard/profiles.html', {'profile': profile})


@login_required
def create_customer_portal_session(request):
    user = request.user
    stripe.api_key = settings.STRIPE_SECRET_KEY
    from dashboard.models import Subscription
    try:
        subscription = Subscription.objects.filter(user=user).order_by('-id').first()
        customer_id = subscription.stripe_customer_id
    except Subscription.DoesNotExist:
        return redirect("/dashboard/") 

    # Create a Stripe Customer Portal session
    session = stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url="http://127.0.0.1:8000/dashboard/",
    )

    return redirect(session.url)

# Products payment

@login_required(login_url='login')
def create_checkout_session(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')  # Get selected product ID
        print(f"Received Product ID: {product_id}")  # Debugging step
        
        if product_id not in PRODUCT_PRICES:
            return render(request, 'dashboard/templates/dashboard/error.html', {'error': 'No valid product selected.'})

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': PRODUCT_PRICES[product_id],
                    'quantity': 1,
                }],
                mode='payment',
                success_url='http://127.0.0.1:8000/success/',
                cancel_url='http://127.0.0.1:8000/cancel/',
            )
            return redirect(checkout_session.url)
        except Exception as error:
            return render(request, 'dashboard/templates/dashboard/error.html', {'error': error})

    return render(request, 'dashboard/templates/dashboard/error.html')
