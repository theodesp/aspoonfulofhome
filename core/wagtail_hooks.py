# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.conf.urls import include, url

from wagtail.wagtailcore import hooks
from wagtail.wagtailadmin.menu import MenuItem

from core.urls import urls


@hooks.register('register_admin_urls')
def urlconf_time():
    return [
        url(r'^theme/$', include(urls, namespace='theme_profiles')),
    ]


@hooks.register('register_settings_menu_item')
def themes():
    return MenuItem('Theme', reverse('theme_profiles:index'),
        classnames='icon icon-cogs', order=10000
    )