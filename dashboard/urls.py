from django.urls import path
from .views import get_logins_per_day

urlpatterns = [
    # path('', dashboard_view, name='dashboard'),
    path('api/logins-per-day/', get_logins_per_day, name='logins_per_day')
]
