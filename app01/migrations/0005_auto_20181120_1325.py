# Generated by Django 2.1.2 on 2018-11-20 05:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_classstudyrecord_student_studentstudyrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='baoming_date',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='报名时间'),
        ),
        migrations.AlterField(
            model_name='classstudyrecord',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='讲师'),
        ),
    ]