# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-26 12:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payday', '0003_auto_20170626_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='create_date',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='entry',
            name='hours',
            field=models.TimeField(),
        ),
    ]
