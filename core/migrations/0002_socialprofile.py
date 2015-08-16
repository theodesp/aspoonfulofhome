# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('social_type', models.CharField(max_length=32, choices=[('facebook', 'facebook'), ('twitter', 'twitter'), ('instagram', 'instagram'), ('googleplus', 'googleplus'), ('linkedin', 'linkedin'), ('dribble', 'dribble'), ('vimeo', 'vimeo'), ('pininterest', 'pininterest'), ('flickr', 'flickr'), ('soundcloud', 'soundcloud'), ('youtube', 'youtube'), ('rss', 'rss')])),
                ('url', models.URLField(help_text='Social link URL', verbose_name='Social link URL', blank=True)),
            ],
        ),
    ]
