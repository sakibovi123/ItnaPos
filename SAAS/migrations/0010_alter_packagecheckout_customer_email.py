# Generated by Django 3.2.9 on 2021-12-06 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SAAS', '0009_packagecheckout_customer_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packagecheckout',
            name='customer_email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
