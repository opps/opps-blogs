#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.core.models import NotUserPublishable, Slugged
from opps.articles.models import Article
from opps.images.models import Image

from .conf import settings


class Blog(NotUserPublishable, Slugged):

    user = models.ManyToManyField(settings.AUTH_USER_MODEL)
    name = models.CharField(_(u"Name"), max_length=140)
    main_image = models.ForeignKey(Image, verbose_name=_(u'Main Image'))
    description = models.TextField(_(u'Description'), blank=True)

    __unicode__ = lambda self: self.name

    def get_absolute_url(self):
        return u"/{}/{}/".format(settings.OPPS_BLOGS_CHANNEL,
                                    self.slug)


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
