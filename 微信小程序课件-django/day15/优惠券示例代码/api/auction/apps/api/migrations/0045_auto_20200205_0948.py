# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2020-02-05 09:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0044_auto_20200205_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='cover',
            field=models.CharField(max_length=128, verbose_name='封面'),
        ),
    ]
