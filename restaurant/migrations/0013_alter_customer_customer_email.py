# Generated by Django 3.2 on 2021-12-02 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0012_rename_email_customer_customer_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]