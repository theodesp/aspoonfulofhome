from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from modelcluster.fields import ParentalKey
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    PageChooserPanel,
    MultiFieldPanel,
    StreamFieldPanel,
    )
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailforms.models import AbstractFormField, AbstractEmailForm
from wagtail.wagtailsearch import index
from wagtail.wagtailcore import blocks

from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase


class LinkField(models.Model):
    """
    A field that links to either a document, image or external page
    """
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )
    document_link = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        related_name='+'
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.document_link:
            return self.document_link.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
        DocumentChooserPanel('document_link')
    ]

    class Meta:
        abstract = True


class CarouselItem(LinkField):
    """
    A field that specifies an image for a carousel
    """
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        related_name='+'
    )

    embed_url = models.URLField("Embed URL", blank=True)

    caption = models.CharField(max_length=255, blank=True)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('embed_url'),
        FieldPanel('caption'),
        MultiFieldPanel(LinkField.panels, "Link"),
    ]

    class Meta:
        abstract = True


class RelatedLink(LinkField):
    """
    A field that specifies a related link
    """
    title = models.CharField(max_length=255, help_text=_("Link title"))

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(LinkField.panels, "Link"),
    ]

    class Meta:
        abstract = True


# Home Page
class HomePage(Page):
    body = RichTextField(blank=True)

HomePage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('body', classname="full"),
    InlinePanel(HomePage, 'related_links', label=_("Related links")),
]
HomePage.promote_panels = Page.promote_panels


# Blog index Page
class BlogIndexPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('BlogIndexPage', related_name='related_links')


class BlogIndexPage(Page):
    intro = models.CharField(max_length=255, help_text=_("Intro"))

    search_fields = Page.search_fields + (
        index.SearchField('intro'),
    )

    subpage_types = ['BlogPage']

    @property
    def blogs(self):
        # Get list of live blog pages that are descendants of this page
        blogs = BlogPage.objects.live().descendant_of(self)
        # Order by most recent date first
        blogs = blogs.order_by('-date')
        return blogs

    def get_context(self, request):
        # Get blogs
        blogs = self.blogs
        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            blogs = blogs.filter(tags__name=tag)
        # Pagination
        page = request.GET.get('page')
        # Show 10 blogs per page
        paginator = Paginator(blogs, 10)
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)
        # Update template context
        context = super(BlogIndexPage, self).get_context(request)
        context['blogs'] = blogs
        return context

    class Meta:
        verbose_name = 'Blog listing'

BlogIndexPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    InlinePanel(BlogIndexPage, 'related_links', label=_("Related links")),
]
BlogIndexPage.promote_panels = Page.promote_panels


# Blog Page
class BlogPageCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('BlogPage', related_name='carousel_items')


class BlogPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('BlogPage', related_name='related_links')


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='tagged_items')


class BlogPage(Page):
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    date = models.DateField("Post date")
    promo_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + (
        index.SearchField('body'),
    )

    parent_page_types = ['BlogIndexPage', 'BlogPage']

    @property
    def blog_index(self):
        """
        Find closest ancestor which is a blog index
        Example self.get_ancestors().type(BlogIndexPage) will return
        [<BlogIndexPage:BlogIndex1>,<BlogIndexPage:BlogIndex2>] and the last
        one is the parent
        """
        return self.get_ancestors().type(BlogIndexPage).last()

BlogPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('date'),
    FieldPanel('body', classname="full"),
    InlinePanel(BlogPage, 'carousel_items', label="Carousel items"),
    InlinePanel(BlogPage, 'related_links', label="Related links"),
]

BlogPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('promo_image'),
    FieldPanel('tags'),
]


class HomePageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('HomePage', related_name='related_links')


class ContactFormField(AbstractFormField):
    page = ParentalKey('ContactFormPage', related_name='form_fields')


class ContactFormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    parent_page_types = []

    class Meta:
        verbose_name = "Contact Form"

ContactFormPage.content_panels = [
    FieldPanel('title', classname="title"),
    FieldPanel('intro', classname="intro"),
    InlinePanel(ContactFormPage, 'form_fields', label=_("Form fields")),
    FieldPanel('thank_you_text', classname="full"),
    MultiFieldPanel([
        FieldPanel('to_address', classname="full"),
        FieldPanel('from_address', classname="full"),
        FieldPanel('subject', classname="full"),
        ], "Email")
]


class StandardPage(Page):
    intro = models.CharField(max_length=255, help_text=_("Intro"))
    body = RichTextField(blank=True)
    promo_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + (
        index.SearchField('intro'),
        index.SearchField('body'),
    )

StandardPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    FieldPanel('body', classname="full"),
    InlinePanel(StandardPage, 'related_links', label="Related links"),
]

StandardPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('promo_image'),
]


class StandardPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('StandardPage', related_name='related_links')


class RecipeIndexPage(Page):

    intro = models.CharField(max_length=255, help_text=_("Intro"))

    search_fields = Page.search_fields + (
        index.SearchField('intro'),
    )

    subpage_types = ['RecipePage']

    @property
    def repipes(self):
        # Get list of live repipes pages that are descendants of this page
        repipes = RecipePage.objects.live().descendant_of(self)
        # Order by most recent date first
        repipes = repipes.order_by('-date')
        return repipes

    def get_context(self, request):
        # Get repipes
        repipes = self.repipes
        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            repipes = repipes.filter(tags__name=tag)
        # Pagination
        page = request.GET.get('page')
        # Show 10 blogs per page
        paginator = Paginator(repipes, 10)
        try:
            repipes = paginator.page(page)
        except PageNotAnInteger:
            repipes = paginator.page(1)
        except EmptyPage:
            repipes = paginator.page(paginator.num_pages)
        # Update template context
        context = super(RecipeIndexPage, self).get_context(request)
        context['repipes'] = repipes
        return context

    class Meta:
        verbose_name = 'Recipes listing'


# Recipe index Page
class RecipeIndexPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('RecipeIndexPage', related_name='related_links')


class RecipePageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('RecipePage', related_name='related_links')


class IngredientsListBlock(blocks.StructBlock):

    ingredient = blocks.CharBlock(help_text=_("Ingredient name"))
    amount = blocks.CharBlock(help_text=_("Ingredient amount in units"))


class RecipeStepsBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text=_("Step title"))
    image = ImageChooserBlock(required=False, help_text=_("Step picture"))
    step = blocks.CharBlock(required=False, help_text=_("Step details"))
    video = EmbedBlock(required=False, help_text=_("Step video"))


# Recipe Page
class RecipePage(Page):
    SERVES_CHOICES = (
        ('1', 'One'),
        ('2', 'Two'),
        ('4-6', 'Four to six'),
        ('6+', 'More than six'),
    )
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    date = models.DateField("Post date")
    recipe = StreamField([
        ('image', ImageChooserBlock(required=False,
            help_text=_("Overview of the ingredients"))),
        ('ingredients', blocks.ListBlock(IngredientsListBlock(),
            template='core/elements/_recipe_ingredients_list.html')),
        ('serves', blocks.ChoiceBlock(
            choices=SERVES_CHOICES, required=True,
            help_text=_("How many people this recipe serves")
        )),
        ('time', blocks.CharBlock(
                help_text=_("How much time it takes to prepare"))),
        ('steps', blocks.ListBlock(RecipeStepsBlock,
                template='core/elements/_recipe_steps_list.html')),
        ])

    promo_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + (
        index.SearchField('body'),
    )

    parent_page_types = ['RecipeIndexPage', 'RecipePage']

RecipePage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('date'),
    FieldPanel('body', classname="full"),
    StreamFieldPanel('recipe'),
    InlinePanel(RecipePage, 'carousel_items', label="Carousel items"),
    InlinePanel(RecipePage, 'related_links', label="Related links"),
]

RecipePage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('promo_image'),
    FieldPanel('tags'),
]


class RecipePageCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('RecipePage', related_name='carousel_items')


class RecipePageTag(TaggedItemBase):
    content_object = ParentalKey('RecipePage', related_name='tagged_items')
