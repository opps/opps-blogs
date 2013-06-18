#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from opps.core.models import NotUserPublishable, Slugged
from opps.articles.models import Article


class Blog(NotUserPublishable, Slugged):

    user = models.ManyToManyField(settings.AUTH_USER_MODEL)
    name = models.CharField(_(u"Name"), max_length=140)


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
        return u"/blog/{}/{}".format(self.blog.slug, self.slug)
