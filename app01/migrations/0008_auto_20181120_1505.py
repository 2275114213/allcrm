# Generated by Django 2.1.2 on 2018-11-20 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0007_customer_baoming_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='baoming_date',
            field=models.DateTimeField(blank=True, default='2018-11-22', null=True, verbose_name='报名时间'),
        ),
    ]
