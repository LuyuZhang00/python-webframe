# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2020-01-17 17:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0040_auto_20200117_1714'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='depositrecord',
            name='py_type',
        ),
        migrations.AddField(
            model_name='depositrecord',
            name='pay_type',
            field=models.SmallIntegerField(choices=[(1, '微信'), (2, '余额')], default=1, verbose_name='支付方式'),
            preserve_default=False,
        ),
    ]
