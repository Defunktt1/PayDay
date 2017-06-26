# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-26 10:47
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(default=datetime.date.today)),
                ('hours', models.DecimalField(decimal_places=2, max_digits=2)),
                ('work_description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_rate', models.DecimalField(decimal_places=2, max_digits=3)),
                ('exchange_rate', models.DecimalField(decimal_places=2, max_digits=3)),
            ],
        ),
    ]