# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch.models import Query, EditorsPick


def search(request):
    # Search
    search_query = request.GET.get('query', None)

    if search_query:
        search_results = Page.objects.live().search(search_query)
        query = Query.get(search_query)
        query.add_hit()
        search_picks = query.editors_picks.all()
    else:
        search_results = Page.objects.none()
        search_picks = EditorsPick.objects.none()

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(search_results, 10)

    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
            search_results = paginator.page(paginator.num_pages)
    return render(request, 'core/search_results.html', {
        'search_query': search_query,
        'search_results': search_results,
        'search_picks': search_picks,
        }
    )