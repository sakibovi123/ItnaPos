# Generated by Django 3.2 on 2021-12-02 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0011_auto_20211202_1351'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='email',
            new_name='customer_email',
        ),
    ]