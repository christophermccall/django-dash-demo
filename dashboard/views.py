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

logger = logging.getLogger(__name__)

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
@ratelimit(key='user_or_ip', rate='10/m')
def get_logins_per_day(request):
    ###subscription blocker
    try:
        sub = Subscription.objects.get(user=request.user)
        if sub.status != "active":
            return JsonResponse({"error": "Subscription required"}, status=403)

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

    ## exception for the subscription try
    except Subscription.DoesNotExist:
        return JsonResponse({"error": "No subscription found"}, status=403)



#checkout session

@login_required(login_url='login')
def create_checkout_session(request):
    user = request.user
    customer = stripe.Customer.create(email=user.email)

    checkout_session = stripe.checkout.Session.create(
        customer=customer.id,
        payment_method_types=["card"],
        line_items=[
            {
                "price": "price_1Qxtc6JNY05FwokpJCjk5rXe",  # Price ID from Stripe
                "quantity": 1,
            }
        ],
        mode="subscription",
        success_url="http://127.0.0.1:8000/success/",
        cancel_url="http://127.0.0.1:8000/cancel/",
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


    if event["type"] == "customer.subscription.updated":
        subscription_data = event["data"]["object"]
        stripe_subscription_id = subscription_data["id"]
        status = subscription_data["status"]

       
        try:
            sub = Subscription.objects.get(stripe_subscription_id=stripe_subscription_id)
            sub.status = status
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