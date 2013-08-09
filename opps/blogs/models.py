#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import get_model
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured

from opps.core.models import NotUserPublishable, Slugged
from opps.articles.models import Article
from opps.images.models import Image

from .conf import settings


class Blog(NotUserPublishable, Slugged):

    user = models.ManyToManyField(settings.AUTH_USER_MODEL)
    name = models.CharField(_(u"Name"), max_length=140)
    main_image = models.ForeignKey(Image, verbose_name=_(u'Main Image'),
                                   blank=True, null=True)
    description = models.TextField(_(u'Description'), blank=True)

    __unicode__ = lambda self: self.name

    def get_absolute_url(self):
        return u"/{}/{}/".format(settings.OPPS_BLOGS_CHANNEL,
                                    self.slug)

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


class BlogPost(Article):
    blog = models.ForeignKey('blogs.Blog')
    content = models.TextField(_(u"Content"))
    albums = models.ManyToManyField(
        'articles.Album',
        null=True, blank=True,
        related_name='blogpoast_albums',
        verbose_name=_(u"Albums")
    )

    class Meta:
        verbose_name = _(u'Blog post')
        verbose_name_plural = _(u'Blog Posts')

    def get_absolute_url(self):
        return u"/{}/{}/{}".format(settings.OPPS_BLOGS_CHANNEL,
                                    self.blog.slug, self.slug)
