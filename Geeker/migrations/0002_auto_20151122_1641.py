# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Geeker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='reviewed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ticket',
            name='solved',
            field=models.BooleanField(default=False),
        ),
    ]
