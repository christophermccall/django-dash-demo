from django.db import models
from django.contrib.auth.models import User

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    page = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"User {self.user.username} performed {self.action} at {self.timestamp}"


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255, unique=True)
    stripe_price_id = models.CharField(max_length=255) 
    status = models.CharField(max_length=50, default="unsubscribed")
    current_period_end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Subscription {self.stripe_subscription_id} - {self.status}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    ORGANIZATION_CHOICES = [
        ('individual', 'Individual'),
        ('for_profit', 'For-Profit'),
        ('non_profit', 'Non-Profit'), # keep the choice but user can't select it
    ]
    organization_type = models.CharField(max_length=20, choices=ORGANIZATION_CHOICES, default='individual')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    ein_number = models.CharField(max_length=9, blank=True, null=True)

    def __str__(self):
        return self.full_name or self.user.username
