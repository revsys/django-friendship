# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('friendship', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('blocked', models.ForeignKey(related_name='blockees', on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('blocker', models.ForeignKey(related_name='blocking', on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Blocker Relationship',
                'verbose_name_plural': 'Blocked Relationships',
            },
        ),
    ]
