# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-26 11:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('payday', '0002_entry_create_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='create_date',
            field=models.TimeField(verbose_name=datetime.datetime(2017, 6, 26, 11, 7, 56, 68502, tzinfo=utc)),
        ),
    ]
