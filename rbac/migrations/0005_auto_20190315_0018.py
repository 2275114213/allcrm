# Generated by Django 2.1.2 on 2019-03-14 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0004_merge_20190315_0014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permission',
            name='code',
        ),
        migrations.AlterField(
            model_name='permission',
            name='url',
            field=models.CharField(max_length=32),
        ),
    ]
