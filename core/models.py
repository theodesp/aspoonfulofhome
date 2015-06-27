from __future__ import unicode_literals

from modelcluster.fields import ParentalKey
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel)
from wagtail.wagtailforms.models import AbstractFormField, AbstractEmailForm

from wagtail_modeltranslation.models import TranslationMixin


class HomePage(TranslationMixin, Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]


class ContactFormField(AbstractFormField):
    page = ParentalKey('ContactFormPage', related_name='form_fields')


class ContactFormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    parent_page_types = []

    class Meta:
        verbose_name = "Contact"

ContactFormPage.content_panels = [
    FieldPanel('title', classname="title"),
    FieldPanel('intro', classname="intro"),
    InlinePanel(ContactFormPage, 'form_fields', label="Form fields"),
    FieldPanel('thank_you_text', classname="full"),
    MultiFieldPanel([
        FieldPanel('to_address', classname="full"),
        FieldPanel('from_address', classname="full"),
        FieldPanel('subject', classname="full"),
        ], "Email")
]