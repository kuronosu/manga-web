# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 23:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('createManga', '0002_auto_20171027_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manga',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
