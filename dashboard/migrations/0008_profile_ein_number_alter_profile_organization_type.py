# Generated by Django 5.1.6 on 2025-04-09 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_remove_subscription_stripe_price_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='ein_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='organization_type',
            field=models.CharField(choices=[('individual', 'Individual'), ('for_profit', 'For-Profit'), ('non_profit', 'Non-Profit')], default='individual', max_length=20),
        ),
    ]
