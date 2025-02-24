from django.urls import path
# from .views import dashboard_view
from . import views
from .views import get_logins_per_day

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('overview/', views.overview, name='overview'),
    path('products/', views.products, name='products'),
    path('activities/', views.activities, name='activities'),
    path('logs/', views.logs, name='logs'),
    path('payouts/', views.payouts, name='payouts'),
    path('profiles/', views.profiles, name='profiles'),
    path('settings/', views.settings, name='settings'),
    path('api/logins-per-day/', get_logins_per_day, name='logins_per_day'),
]
