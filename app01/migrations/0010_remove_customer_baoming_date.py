# Generated by Django 2.1.2 on 2018-11-20 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0009_auto_20181120_1512'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='baoming_date',
        ),
    ]
