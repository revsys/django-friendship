# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('followee', models.ForeignKey(related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('follower', models.ForeignKey(related_name='following', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Following Relationship',
                'verbose_name_plural': 'Following Relationships',
            },
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('from_user', models.ForeignKey(related_name='_unused_friend_relation', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(related_name='friends', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Friend',
                'verbose_name_plural': 'Friends',
            },
        ),
        migrations.CreateModel(
            name='FriendshipRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField(verbose_name='Message', blank=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('rejected', models.DateTimeField(null=True, blank=True)),
                ('viewed', models.DateTimeField(null=True, blank=True)),
                ('from_user', models.ForeignKey(related_name='friendship_requests_sent', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(related_name='friendship_requests_received', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Friendship Request',
                'verbose_name_plural': 'Friendship Requests',
            },
        ),
        migrations.AlterUniqueTogether(
            name='friendshiprequest',
            unique_together=set([('from_user', 'to_user')]),
        ),
        migrations.AlterUniqueTogether(
            name='friend',
            unique_together=set([('from_user', 'to_user')]),
        ),
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together=set([('follower', 'followee')]),
        ),
    ]
