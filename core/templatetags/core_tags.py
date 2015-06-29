from django.utils.http import urlencode
from django import template

from wagtail.wagtailcore.models import Page, Site

register = template.Library()


sharer_links = {
    'facebook': 'http://www.facebook.com/sharer.php?u={absolute_url}',
    'twitter':
    'https://twitter.com/intent/tweet?original_referer={absolute_url}&amp;url={absolute_url}',
    'googleplus':
    'https://plusone.google.com/_/+1/confirm?hl=en-US&amp;url={absolute_url}',
}


@register.inclusion_tag('core/elements/_pagetitle.html', takes_context=True)
def pagetitle(context):
    self = context.get('self')
    site = Site.objects.get(is_default_site=True)
    if self.pk == site.root_page.pk:
        pagetitle = None
    else:
        pagetitle = self.title
    return {
        'pagetitle': pagetitle,
        'request': context['request'],
    }


@register.inclusion_tag('core/elements/_breadcrumbs.html', takes_context=True)
def breadcrumbs(context):
    """
    Generate page breadcrumbs not including the home page,
    as displaying breadcrumbs there is irrelevant.
    """
    self = context.get('self')
    if self is None or self.depth <= 2:
        ancestors = ()
    else:
        ancestors = Page.objects.ancestor_of(
        self, inclusive=True).filter(depth__gte=2)
    return {
        'ancestors': ancestors,
        'request': context['request'],
    }


@register.inclusion_tag('core/elements/_social_list.html')
def social_list(page):

    if page is None:
        social_links = None
    else:
        social_links = {
            k: v.format(absolute_url=page.full_url)
            for k, v in list(sharer_links.items())
        }
    return {
        'social_links': social_links,
    }
