# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-18 01:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manageManga', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='manga',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
