# -*- coding: utf-8 -*-
from django.shortcuts import render


def index(request):
    return render(request, 'core/theme_settings.html', {})


def create(request):
    pass


def edit(request):
    pass

