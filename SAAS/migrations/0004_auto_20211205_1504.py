# Generated by Django 3.2 on 2021-12-05 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SAAS', '0003_auto_20211204_1713'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='package',
            options={},
        ),
        migrations.AddField(
            model_name='package',
            name='package_description',
            field=models.TextField(null=True),
        ),
    ]
