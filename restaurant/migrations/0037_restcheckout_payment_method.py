# Generated by Django 3.2.9 on 2021-12-07 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0036_auto_20211207_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='restcheckout',
            name='payment_method',
            field=models.CharField(choices=[('CASH', 'CASH'), ('Credit Card', 'Credit Card'), ('bKash', 'bKash'), ('Nagad', 'Nagad')], max_length=120, null=True),
        ),
    ]