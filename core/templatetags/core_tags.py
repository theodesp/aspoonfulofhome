from django import template

from wagtail.wagtailcore.models import Page, Site

register = template.Library()


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
