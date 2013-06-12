#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.articles.models import Article


class BlogPost(Article):
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
        return u"/blog/{}/{}/{}".format(self.user.username,
                                        self.channel_long_slug, self.slug)
