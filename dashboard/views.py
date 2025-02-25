from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.http import JsonResponse
from .models import UserActivity
import logging

logger = logging.getLogger(__name__)

# Dashboard - Requires Login
@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'dashboard/index.html')

def index(request):
    return render(request, 'index.html')


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
            return redirect(reverse('dashboard'))

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
        messages.info(request, "You have been logged out successfully.")

    return redirect('login')

# Get login counts per day
def get_logins_per_day(request):
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
