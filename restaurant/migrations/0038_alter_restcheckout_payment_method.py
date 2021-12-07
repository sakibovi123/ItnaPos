# Generated by Django 3.2.9 on 2021-12-07 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0037_restcheckout_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restcheckout',
            name='payment_method',
            field=models.CharField(choices=[('CASH', 'CASH'), ('Credit Card', 'Credit Card'), ('bKash', 'bKash'), ('Nagad', 'Nagad')], default='CASH', max_length=120, null=True),
        ),
    ]