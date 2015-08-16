# -*- coding: utf-8 -*-
from django.conf.urls import url
from core.views import theme_profiles

urlpatterns = [
url(r'^$', theme_profiles.index, name='index'),
url(r'^add/$', theme_profiles.create, name='add'),
url(r'^([^\/]+)/$', theme_profiles.edit, name='edit'),
]