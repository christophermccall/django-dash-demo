from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
import uuid


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    page = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"User {self.user.username} performed {self.action} at {self.timestamp}"


def get_default_user():
    user, created = User.objects.get_or_create(username="default_user", email="default@example.com")
    return user.id 

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)
    stripe_customer_id = models.CharField(max_length=255, null=True, blank=True)
    stripe_subscription_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    stripe_price_ids = ArrayField(models.CharField(max_length=255), default=list)  # Store multiple price IDs
    stripe_subscription_item_ids = ArrayField(models.CharField(max_length=255), default=list, blank=True)  # Multiple items
    stripe_checkout_session_id = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=50, default="pending")
    current_period_end = models.DateTimeField(null=True, blank=True)
    tracker_request_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Subscription: {self.user} - {self.status}" if self.user else f"Subscription: {self.status}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    ORGANIZATION_CHOICES = [
        ('for_profit', 'For-Profit'),
        ('non_profit', 'Non-Profit'),
    ]
    organization_type = models.CharField(max_length=20, choices=ORGANIZATION_CHOICES, default='for_profit')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.full_name or self.user.username