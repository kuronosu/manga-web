# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-19 04:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manageManga', '0007_auto_20171119_0441'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chapter',
            name='chapter_number',
        ),
    ]
