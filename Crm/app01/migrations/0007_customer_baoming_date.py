# Generated by Django 2.1.2 on 2018-11-20 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_remove_customer_baoming_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='baoming_date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='报名时间'),
        ),
    ]