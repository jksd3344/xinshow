# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='feedgo',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('Stime', models.CharField(unique=True, max_length=32)),
                ('Etime', models.CharField(unique=True, max_length=32)),
                ('Whether', models.CharField(unique=True, max_length=32)),
                ('Remarks', models.CharField(unique=True, max_length=32)),
                ('ucid', models.IntegerField(null=True, blank=True)),
                ('oid', models.IntegerField(null=True, blank=True)),
                ('setbacks', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'feedgo',
                'managed': False,
            },
        ),
    ]
