# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-11 00:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_remove_colegio_slogan'),
    ]

    operations = [
        migrations.AddField(
            model_name='profesion',
            name='prueba',
            field=models.CharField(default='prueba', max_length=100, unique=True),
            preserve_default=False,
        ),
    ]
