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