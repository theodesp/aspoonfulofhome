# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailsnippets.models import register_snippet


SOCIAL_PROFILE_CHOICES = (
        ('facebook', 'facebook'),
        ('twitter', 'twitter'),
        ('instagram', 'instagram'),
        ('googleplus', 'googleplus'),
        ('linkedin', 'linkedin'),
        ('dribble', 'dribble'),
        ('vimeo', 'vimeo'),
        ('pininterest', 'pininterest'),
        ('flickr', 'flickr'),
        ('soundcloud', 'soundcloud'),
        ('youtube', 'youtube'),
        ('rss', 'rss'),
    )


@register_snippet
class SocialProfile(models.Model):
    social_type = models.CharField(choices=SOCIAL_PROFILE_CHOICES)

    url = models.URLField("Social link URL",
        blank=True, help_text=_("Social link URL"))

    panels = [
        FieldPanel('url'),
        FieldPanel('social_type'),
  ]

    def __unicode__(self):
        return self.social_type