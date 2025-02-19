from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import UserActivity
import logging
logger = logging.getLogger(__name__)

# Create your views here.
@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'dashboard/index.html')


# def HomePage(request):
#     return render (request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confirm password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            # logger for the console
            logger.info(f"New user {uname} registered with email {email}.")
            #logging for the database
            UserActivity.objects.create(
                user=request.user,
                action="account creation",
                ip_address=request.META.get('REMOTE_ADDR'),
                page=request.path
            )

            return redirect('login')

    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            # logger for the console
            logger.info(f"user {username} logged in")
            #logging for the database
            UserActivity.objects.create(
                user=request.user,
                action="logged in",
                ip_address=request.META.get('REMOTE_ADDR'),
                page=request.path
            )

            return redirect('dashboard')
        else:
            logger.warning(f"Failed login attempt for username {username}")
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    username = request.user.username
    logout(request)
    # logger for the console
    logger.info(f"user {username} logged out")
    #logging for the database
    UserActivity.objects.create(
        user=request.user,
        action="logged out",
        ip_address=request.META.get('REMOTE_ADDR'),
        page=request.path
    )

    return redirect('login')