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

stripe.api_key = settings.STRIPE_SECRET_KEY

logger = logging.getLogger(__name__)


def rate_limit(request, key_prefix="rate_limit", limit=10, timeout=60):
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

            messages.success(request, "Login successful!")
            return redirect('dashboard')

        else:
            logger.warning(f"Failed login attempt for username {username}")
            messages.error(request, "Username or Password is incorrect!")
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

    rate_limit_response = rate_limit(request, key_prefix="logins", limit=10, timeout=60)
    if rate_limit_response:
        return rate_limit_response

    try:
            login_data = (UserActivity.objects
                        .filter(action='logged in')
                        .annotate(login_date=TruncDate('timestamp'))
                        .values('login_date')
                        .annotate(login_count=Count('id'))
                        .order_by('login_date'))

            logger.info(f"Login data: {login_data}")

            result = [{"login_date": entry['login_date'].strftime('%Y-%m-%d'), "login_count": entry['login_count']} for entry in login_data]

            return JsonResponse(result, safe=False)

    except Exception as e:
        logger.error(f"Error in get_logins_per_day view: {str(e)}")
        return JsonResponse({"error": "An error occurred while processing your request. Please try again."}, status=500)
    # ###subscription blocker
    # try:
    #     sub = Subscription.objects.get(user=request.user)
    #     if sub.status != "active":
    #         return JsonResponse({"error": "Subscription required"}, status=403)
    #         ## exception for the subscription try
    # except Subscription.DoesNotExist:


        return JsonResponse({"error": "No subscription found"}, status=403)



#checkout session

@login_required(login_url='login')
def create_checkout_session(request):
    user = request.user
    

    # Check if user already has a subscription
    existing_subscription = Subscription.objects.filter(user=user).first()

    # If the user has an existing subscription, update it instead of creating a new customer
    if existing_subscription and existing_subscription.status == "active":
        return redirect("/dashboard/")  # Redirect to dashboard if already subscribed

    # Create a Stripe customer if not already stored
    customer = stripe.Customer.create(email=user.email)
    checkout_session = stripe.checkout.Session.create(
        customer=customer.id,
        payment_method_types=["card"],
        line_items=[
            {
                "price": "price_1Qxtc6JNY05FwokpJCjk5rXe",
                "quantity": 1,
            }
        ],
        mode="subscription",
        success_url="http://127.0.0.1:8000/success/",
        cancel_url="http://127.0.0.1:8000/cancel/",
    )

    # Save or update the Subscription in the database
    if existing_subscription:
        existing_subscription.stripe_customer_id = customer.id
        existing_subscription.stripe_subscription_id = checkout_session.id
        existing_subscription.stripe_price_id = "price_1Qxtc6JNY05FwokpJCjk5rXe"
        existing_subscription.status = "pending"
        existing_subscription.save()
    else:
        Subscription.objects.create(
            user=user,
            stripe_customer_id=customer.id,
            stripe_subscription_id=checkout_session.id,
            stripe_price_id="price_1Qxtc6JNY05FwokpJCjk5rXe",
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

    # New Subscription Created (from Checkout)
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_id = session["customer"]
        subscription_id = session["subscription"]

        try:
            # Find existing subscription or create a new one
            sub, created = Subscription.objects.get_or_create(
                stripe_customer_id=customer_id,
                defaults={"stripe_subscription_id": subscription_id, "status": "active"},
            )
            if not created:
                sub.stripe_subscription_id = subscription_id
                sub.status = "active"
                sub.save()
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # Subscription Updated
    elif event["type"] == "customer.subscription.updated":
        subscription_data = event["data"]["object"]
        stripe_subscription_id = subscription_data["id"]
        status = subscription_data["status"]

        try:
            sub = Subscription.objects.get(stripe_subscription_id=stripe_subscription_id)
            sub.status = status
            sub.save()
        except Subscription.DoesNotExist:
            pass

    # Subscription Canceled
    elif event["type"] == "customer.subscription.deleted":
        subscription_data = event["data"]["object"]
        stripe_subscription_id = subscription_data["id"]

        try:
            sub = Subscription.objects.get(stripe_subscription_id=stripe_subscription_id)
            sub.status = "canceled"
            sub.save()
        except Subscription.DoesNotExist:
            pass

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
        subscription = Subscription.objects.get(user=user)
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

def checkout_session(request):
    if request.method == 'POST':
        try:
            # Get the product details from the POST request
            product_name = request.POST.get('name')
            product_price = Decimal(request.POST.get('price')) * 100  # Convert to cents for Stripe
            product_description = request.POST.get('description')

            user_email = request.user.email  

            # Create a Stripe checkout session for a one-time product purchase (payment)
            checkout_session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(product_price),  # Stripe requires the price in cents
                        'product_data': {
                            'name': product_name,
                            'description': product_description,
                            'images': ['https://example.com/product_image.jpg'],  # Replace with actual image URL
                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',  # Set mode to 'payment' for one-time purchase
                success_url="http://127.0.0.1:8000/success/",
                cancel_url="http://127.0.0.1:8000/cancel/",
                customer_email=user_email,
            )

            # Redirect to Stripe Checkout session
            return redirect(checkout_session.url)

        except Exception as error:
            return render(request, 'public/error.html', {'error': error})

    return render(request, 'public/cancel.html')
