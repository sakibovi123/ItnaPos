# Generated by Django 3.2 on 2021-12-05 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SAAS', '0006_remove_packagecheckout_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='packagecheckout',
            name='bkash_number',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='packagecheckout',
            name='bkash_transaction_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='packagecheckout',
            name='nagad_number',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='packagecheckout',
            name='nagad_transaction_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
