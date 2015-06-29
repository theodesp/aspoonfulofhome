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


def has_menu_children(page):
    """
    Check if page has children that can appear in menus
    """
    return page.get_children().live().in_menu().exists()


# Retrieves the top menu items - the immediate children of the parent page
@register.inclusion_tag('core/elements/_top_menu.html', takes_context=True)
def top_menu(context, parent, calling_page=None):
    menuitems = parent.get_children().live().in_menu().order_by('title')
    for menuitem in menuitems:
        menuitem.show_dropdown = has_menu_children(menuitem)
        # The template engine can pass an empty string to calling_page
        # if the variable passed as calling_page does not exist.
        menuitem.active = (
            calling_page.url.startswith(menuitem.url)
            if calling_page else False
        )
    return {
        'calling_page': calling_page,
        'menuitems': menuitems,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


@register.inclusion_tag(
    'core/elements/_top_menu_children.html',
    takes_context=True
)
def top_menu_children(context, parent):
    """
    Retrieves the children of the top menu items for the drop downs
    """
    menuitems_children = parent.get_children()
    menuitems_children = menuitems_children.live().in_menu()
    return {
        'parent': parent,
        'menuitems_children': menuitems_children,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
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
