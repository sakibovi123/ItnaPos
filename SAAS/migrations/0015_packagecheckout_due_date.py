# Generated by Django 3.2.9 on 2021-12-07 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SAAS', '0014_auto_20211206_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='packagecheckout',
            name='due_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
