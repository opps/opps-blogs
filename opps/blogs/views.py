#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.sites.models import get_current_site
from django.utils import timezone

from opps.articles.views.generic import OppsDetail, OppsList

from opps.blogs.models import Blog, BlogPost


class PostBlogList(OppsList):
    model = BlogPost
    type = "blogs"
    channel_long_slug = []
    channel = None

    def get_template_names(self):
        templates = super(PostBlogList, self).get_template_names()
        domain_folder = self.get_template_folder()
        templates = ['{}/blog/{}/{}.html'.format(
            domain_folder,
            self.kwargs['user__useraname'],
            self.paginate_suffix
        )] + templates
        return templates

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
    model = BlogPost
    type = "blogs"
    channel_long_slug = []
    channel = None

    def get_template_names(self):
        templates = super(PostBlogDetail, self).get_template_names()
        domain_folder = self.get_template_folder()
        templates = ['{}/blog/{}/{}.html'.format(
            domain_folder,
            self.kwargs['user__useraname'],
            self.paginate_suffix
        )] + templates
        return templates

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
