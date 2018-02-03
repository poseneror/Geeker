# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid
import phonenumber_field.modelfields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, blank=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('review_text', models.TextField(blank=True)),
                ('review_rating', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', null=True, blank=True)),
                ('email', models.EmailField(max_length=255, verbose_name='email address', unique=True, db_index=True)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('first_name', models.CharField(max_length=100, blank=True)),
                ('last_name', models.CharField(max_length=100, blank=True)),
                ('image', models.ImageField(upload_to='profile_pictures', blank=True)),
                ('website', models.URLField(help_text='ex: http://www.yoursite.com', blank=True)),
                ('field', models.CharField(max_length=2, choices=[('SE', 'Software Engineer'), ('EE', 'Electrical Engineer'), ('HE', 'Hardware Expert'), ('NE', 'Network Expert')], blank=True)),
                ('info', models.TextField(blank=True)),
                ('available', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_supplier', models.BooleanField(verbose_name='supplier', default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('freelancers', models.ManyToManyField(related_name='freelancers_rel_+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='ticket',
            name='assigned',
            field=models.ForeignKey(related_name='expert', blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ticket',
            name='supplier',
            field=models.ForeignKey(related_name='supplier', blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
