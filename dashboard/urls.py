from django.urls import path
from .views import dashboard_view
from .views import LogoutPage
from .views import get_logins_per_day
from dashboard.views import index

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('logout/', LogoutPage, name='logout'),
    path('api/logins-per-day/', get_logins_per_day, name='logins_per_day')
]
