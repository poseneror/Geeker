# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Geeker', '0003_auto_20151123_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketrequest',
            name='ticket',
            field=models.OneToOneField(related_query_name='ticketrequest', to='Geeker.Ticket'),
        ),
    ]
