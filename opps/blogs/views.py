#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.sites.models import get_current_site
from django.utils import timezone

from opps.articles.views.generic import OppsDetail, OppsList

from .models import PostBlog


class PostBlogList(OppsList):
    model = PostBlog
    type = "blogs"
    channel_long_slug = []
    channel = None

    @property
    def queryset(self):
        self.site = get_current_site(self.request).domain
        self.long_slug = None
        self.article = self.model.objects.filter(
            site_domain=self.site,
            user__useraname=self.kwargs['user__useraname'],
            date_available__lte=timezone.now(),
            published=True)
        return self.article


class PostBlogDetail(OppsDetail):
    model = PostBlog
    type = "blogs"
    channel_long_slug = []
    channel = None

    @property
    def queryset(self):
        self.site = get_current_site(self.request).domain
        self.long_slug = None
        self.article = self.model.objects.filter(
            site_domain=self.site,
            user__useraname=self.kwargs['user__useraname'],
            slug=self.kwargs['slug'],
            date_available__lte=timezone.now(),
            published=True)
        return self.article
