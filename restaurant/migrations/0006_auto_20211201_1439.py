# Generated by Django 3.2 on 2021-12-01 08:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0005_auto_20211201_1409'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restcheckout',
            name='quantity',
        ),
        migrations.CreateModel(
            name='DueModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_note', models.TextField()),
                ('submission_date', models.DateField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.customer')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
