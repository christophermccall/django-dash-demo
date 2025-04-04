from django.urls import path

from .views import dashboard_view
from .views import LogoutPage
from . import views
from .views import get_logins_per_day, create_customer_portal_session, create_checkout_session,create_sub_checkout_session

urlpatterns = [

    path('', dashboard_view, name='dashboard'),
    path('logout/', LogoutPage, name='logout'),
    path('api/logins-per-day/', get_logins_per_day, name='logins_per_day'),
    path('', views.dashboard_view, name='dashboard'),
    path('overview/', views.overview, name='overview'),
    path('products/', views.products, name='products'),
    path('activities/', views.activities, name='activities'),
    path('logs/', views.logs, name='logs'),
    path('payouts/', views.payouts, name='payouts'),
    path('profiles/', views.profiles, name='profiles'),
    path('settings/', views.user_settings, name='user_settings'),
    path('api/logins-per-day/', get_logins_per_day, name='logins_per_day'),
    path('checkout-session/', views.create_checkout_session, name='checkout_session'),
    path('create_checkout_session/',views.create_checkout_session, name='create_checkout_session'),
    path('create_sub_checkout_session/',views.create_sub_checkout_session, name='create_sub_checkout_session'),
    path('customer-portal/', views.create_customer_portal_session, name='create_customer_portal_session'),
    path('pricing/', views.price_page, name='price_page')
]
