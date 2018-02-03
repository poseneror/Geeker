# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Geeker', '0002_auto_20151122_1641'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmploymentRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='TicketRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='response',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ticketrequest',
            name='assigned',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ticketrequest',
            name='ticket',
            field=models.ForeignKey(to='Geeker.Ticket'),
        ),
        migrations.AddField(
            model_name='employmentrequest',
            name='provider',
            field=models.ForeignKey(related_name='provider', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='employmentrequest',
            name='user',
            field=models.ForeignKey(related_name='it_expert', to=settings.AUTH_USER_MODEL),
        ),
    ]
