# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-18 14:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gost_app', '0011_auto_20160418_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guest',
            name='friends_list',
            field=models.ManyToManyField(blank=True, to='gost_app.Guest'),
        ),
    ]