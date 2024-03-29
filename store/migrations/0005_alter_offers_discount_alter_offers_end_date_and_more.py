# Generated by Django 4.1.4 on 2023-02-10 06:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_rename_dicount_offers_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offers',
            name='discount',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='offers',
            name='end_date',
            field=models.DateField(default=datetime.date.today, null=True),
        ),
        migrations.AlterField(
            model_name='offers',
            name='start_date',
            field=models.DateField(default=datetime.date.today, null=True),
        ),
    ]
