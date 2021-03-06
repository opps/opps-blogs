#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import get_model
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from mptt.models import MPTTModel, TreeForeignKey

from opps.core.models import NotUserPublishable, Slugged
from opps.articles.models import Article
from opps.images.models import Image
from opps.multimedias.models import Audio, Video

from .conf import settings


class Category(MPTTModel, NotUserPublishable, Slugged):
    blog = models.ForeignKey('blogs.Blog', related_name='categories')
    name = models.CharField(_("Name"), max_length=140)
    long_slug = models.SlugField(_("Path name"), max_length=250,
                                 db_index=True)
    show_in_menu = models.BooleanField(_("Show in menu?"), default=False)
    group = models.BooleanField(_("Group sub-channel?"), default=False)
    order = models.IntegerField(_("Order"), default=0)
    parent = TreeForeignKey(
        'self',
        related_name='subchannel',
        null=True, blank=True,
        verbose_name=_('Parent'),
        limit_choices_to={
            'parent__isnull': True,  # We don't allow subsubcategories
        }
    )

    class Meta:
        unique_together = ("site", "blog", "long_slug")
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name', 'parent__id', 'published']

    class MPTTMeta:
        order_insertion_by = ['order', 'name']

    def __unicode__(self):
        """ Uniform resource identifier
        http://en.wikipedia.org/wiki/Uniform_resource_identifier
        """
        if self.parent:
            return "/{}/{}/".format(self.parent.slug, self.slug)
        return "/{}/".format(self.slug)

    def get_absolute_url(self):
        return "/{}/{}{}".format(settings.OPPS_BLOGS_CHANNEL,
                                 self.blog.slug, self.__unicode__())

    @property
    def root(self):
        return self.get_root()

    def _make_long_slug(self):
        if self.parent:
            return '{}/{}'.format(self.parent.slug, self.slug)
        return self.slug

    def clean(self):
        """Validate uniqueness based on unique_together
        """
        # Do not use self.long_slug here, it might don't exists yet,
        # use self._make_long_slug() instead.
        try:
            category_list = Category.objects.filter(
                site=self.site,
                blog=self.blog,
                long_slug=self._make_long_slug()
            )
        except ObjectDoesNotExist:
            pass
        else:
            if self.pk:
                category_list = category_list.exclude(pk=self.pk)
            if category_list.exists():
                raise ValidationError(
                    _('The slug chosen already exists. Please try another.'))
        finally:
            super(Category, self).clean()

    def save(self, *args, **kwargs):
        self.long_slug = self._make_long_slug()
        super(Category, self).save(*args, **kwargs)

    def validate_slug(self):
        # Prevent Slugged.validate_slug by append a suffix to slugs
        # that are not unique. Our uniqueness here are based on
        # long_slug.
        pass


class Blog(NotUserPublishable, Slugged):
    LAYOUT_MODES = (
        ('default', _('Default')),
        ('resumed', _('Resumed')),
        ('mix', _('Mix')),
    )

    user = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                  verbose_name=_('Users'))
    name = models.CharField(_("Name"), max_length=140)
    main_image = models.ForeignKey(Image, verbose_name=_('Main Image'),
                                   blank=True, null=True)
    description = models.TextField(_('Description'), blank=True)
    type = models.CharField(_('Blog Type'), max_length=200,
                            choices=settings.OPPS_BLOGS_TYPES)
    layout_mode = models.CharField(_('Layout mode'), max_length=200,
                                   default='default', choices=LAYOUT_MODES)
    related_blogs = models.ManyToManyField(
        "blogs.Blog",
        verbose_name=_('Related blogs'),
        null=True,
        blank=True,
        related_name="blog_relatedblogs",
        through="blogs.BlogRelated")
    related_channels = models.ManyToManyField(
        "channels.Channel",
        verbose_name=_('Related channels'),
        null=True,
        blank=True,
        related_name="blog_relatedchannels",
        through="blogs.BlogChannelRelated")
    external = models.BooleanField(
        verbose_name=_('External'),
        default=False)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/{}/{}/".format(settings.OPPS_BLOGS_CHANNEL, self.slug)

    def get_profile(self):
        if not settings.OPPS_BLOGS_PROFILE:
            raise ImproperlyConfigured(_('OPPS_BLOG_PROFILE was not found on'
                                         ' settings'))
        try:
            app_label, model_name = settings.OPPS_BLOGS_PROFILE.split('.')
        except ValueError:
            raise ImproperlyConfigured(_('OPPS_BLOGS_PROFILE must be of the'
                                         ' form "app_label.model_name"'))

        Profile = get_model(app_label, model_name)
        if Profile is None:
            raise ImproperlyConfigured("OPPS_BLOGS_PROFILE refers to model"
                                       " '%s' that has not been installed" %
                                       settings.OPPS_BLOGS_PROFILE)

        return Profile.objects.get(blog=self)

    # Template helpers  - Perhaps a templatetag should be better?
    def get_links(self):
        return self.links.filter(published=True)

    def get_latest(self):
        try:
            return self.blogpost_set.latest()
        except:
            return None

    def get_categories(self):
        return self.categories.filter(published=True)

    def get_menu_categories(self):
        return self.categories.filter(published=True, show_in_menu=True)

    class Meta:
        verbose_name = _('Blog')
        verbose_name_plural = _('Blogs')
        ordering = ('name', )


class BlogRelated(models.Model):
    blog = models.ForeignKey(
        "blogs.Blog",
        null=True,
        blank=True,
        verbose_name=_("Blog"),
        related_name="blogrelated_blog",
        on_delete=models.SET_NULL)

    related = models.ForeignKey(
        "blogs.Blog",
        null=True,
        blank=True,
        verbose_name=_("Related blog"),
        related_name="blogrelated_related",
        on_delete=models.SET_NULL)

    order = models.PositiveIntegerField(_('Order'), default=0)

    class Meta:
        verbose_name = _('Related blog')
        verbose_name_plural = _('Related blogs')
        ordering = ('order',)


class BlogChannelRelated(models.Model):
    blog = models.ForeignKey("blogs.Blog", verbose_name=_("Blog"))

    related = models.ForeignKey(
        "channels.Channel", verbose_name=_("Related channel"))

    order = models.PositiveIntegerField(_('Order'), default=0)

    class Meta:
        verbose_name = _('Related channel')
        verbose_name_plural = _('Related channels')
        ordering = ('order',)


class BlogPost(Article):
    blog = models.ForeignKey('blogs.Blog', verbose_name=_('Blog'))
    content = models.TextField(_("Content"))
    category = models.ForeignKey('blogs.Category', blank=True, null=True,
                                 verbose_name=_('Category'))
    albums = models.ManyToManyField(
        'articles.Album',
        null=True, blank=True,
        related_name='blogpoast_albums',
        verbose_name=_("Albums")
    )
    videos = models.ManyToManyField(Video, blank=True, null=True,
                                    through='BlogPostVideo')
    audios = models.ManyToManyField(Audio, blank=True, null=True,
                                    through='BlogPostAudio')

    accept_comments = models.BooleanField(_('Accept comments?'),
                                          default=True)

    related_blogposts = models.ManyToManyField(
        'blogs.BlogPost',
        null=True,
        blank=True,
        related_name='blogpost_relatedblogposts',
        through='blogs.BlogPostRelated',
    )

    class Meta:
        ordering = ['-date_available']
        verbose_name = _('Blog post')
        verbose_name_plural = _('Blog Posts')
        get_latest_by = 'date_available'

    def get_absolute_url(self):
        try:
            category = self.category
            slug = category.long_slug
        except AttributeError:
            slug = 'sem-categoria'

        return "/{}/{}/{}/{}.html".format(settings.OPPS_BLOGS_CHANNEL,
                                          self.blog.slug, slug, self.slug)


class BlogPostRelated(models.Model):
    blogpost = models.ForeignKey(
        'blogs.BlogPost',
        verbose_name=_('BlogPost'),
        null=True,
        blank=True,
        related_name='blogpostrelated_blogpost',
        on_delete=models.SET_NULL
    )
    related = models.ForeignKey(
        'blogs.BlogPost',
        verbose_name=_('Related BlogPost'),
        null=True,
        blank=True,
        related_name='blogpostrelated_related',
        on_delete=models.SET_NULL
    )
    order = models.PositiveIntegerField(_('Order'), default=0)

    class Meta:
        verbose_name = _('Related content')
        verbose_name_plural = _('Related contents')
        ordering = ('order',)

    def __unicode__(self):
        if self.related and self.blogpost:
            return "{0}->{1}".format(self.related.slug, self.blogpost.slug)
        return None


class BlogLink(NotUserPublishable):
    blog = models.ForeignKey('blogs.Blog', related_name='links')
    name = models.CharField(_("Name"), max_length=140)
    link = models.URLField(_('Link'))

    def __unicode__(self):
        return "{} - {}".format(self.name, self.link)

    class Meta:
        verbose_name = _('Blog Link')
        verbose_name_plural = _('Blog Links')


class BlogPostVideo(models.Model):
    blogpost = models.ForeignKey('blogs.BlogPost', null=True, blank=True,
                                 verbose_name=_('Blog'),
                                 on_delete=models.SET_NULL)
    video = models.ForeignKey(Video, null=True, blank=True,
                              verbose_name=_('Video'),
                              on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('Blogpost Video')
        verbose_name_plural = _('Blogpost Videos')


class BlogPostAudio(models.Model):
    blogpost = models.ForeignKey('blogs.BlogPost', null=True, blank=True,
                                 verbose_name=_('Blog'),
                                 on_delete=models.SET_NULL)
    audio = models.ForeignKey(Audio, verbose_name=_('Audio'), null=True,
                              blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('Blogpost Audio')
        verbose_name_plural = _('Blogpost Audios')


@receiver(post_save, sender=Blog)
def create_blog_profile(sender, **kwargs):
    if not settings.OPPS_BLOGS_PROFILE:
        return
    if not kwargs.get('created'):
        return

    try:
        app_label, model_name = settings.OPPS_BLOGS_PROFILE.split('.')
    except ValueError:
        return

    instance = kwargs.get('instance')
    Profile = get_model(app_label, model_name)
    Profile.objects.create(blog=instance)
