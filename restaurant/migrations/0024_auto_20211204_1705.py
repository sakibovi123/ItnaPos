# Generated by Django 3.2 on 2021-12-04 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SAAS', '0002_alter_shop_user'),
        ('restaurant', '0023_restcheckout_sold_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restcheckout',
            name='sold_by',
        ),
        migrations.AddField(
            model_name='restcheckout',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='SAAS.shop'),
        ),
    ]
