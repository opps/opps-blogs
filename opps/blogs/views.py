#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.sites.models import get_current_site
from django.utils import timezone

from opps.views.generic.list import ListView
from opps.views.generic.detail import DetailView

from opps.blogs.models import BlogPost, Blog


class BlogList(ListView):
    model = Blog
    channel_long_slug = []
    channel = None
    paginate_suffix = 'list'

    def get_template_names(self):
        templates = super(BlogList, self).get_template_names()
        domain_folder = self.get_template_folder()
        templates = ['{}/blogs/{}/authors.html'.format(
            domain_folder,
            self.kwargs['blog__slug'],
        ), '{}/blogs/authors.html'.format(
            domain_folder
        )] + templates
        print templates
        return templates

    def get_queryset(self):
        self.site = get_current_site(self.request)
        self.long_slug = self.kwargs['blog__slug'],
        self.blogs = self.model.objects.filter(
            site_domain=self.site.domain,
            slug=self.long_slug,
            date_available__lte=timezone.now(),
            published=True)

        return self.blogs


class BlogPostList(ListView):
    model = BlogPost
    type = "blogs"
    channel_long_slug = []
    channel = None
    paginate_suffix = 'list'

    def get_template_names(self):
        templates = super(BlogPostList, self).get_template_names()
        domain_folder = self.get_template_folder()
        templates = ['{}/blogs/{}/{}.html'.format(
            domain_folder,
            self.kwargs['blog__slug'],
            self.paginate_suffix
        ), '{}/blogs/{}.html'.format(
            domain_folder,
            self.paginate_suffix)] + templates

        return templates

    def get_queryset(self):
        self.site = get_current_site(self.request)
        self.long_slug = self.kwargs['blog__slug'],
        self.article = self.model.objects.filter(
            site_domain=self.site.domain,
            blog__slug=self.long_slug,
            date_available__lte=timezone.now(),
            published=True)

        return self.article


class BlogPostDetail(DetailView):
    model = BlogPost
    type = "blogs"
    channel_long_slug = []
    channel = None
    paginate_suffix = 'detail'

    def get_template_names(self):
        templates = super(BlogPostDetail, self).get_template_names()
        domain_folder = self.get_template_folder()
        templates = ['{}/blogs/{}/{}.html'.format(
            domain_folder,
            self.long_slug,
            self.paginate_suffix
        ), '{}/blogs/{}.html'.format(
            domain_folder,
            self.paginate_suffix)] + templates
        return templates

    def get_queryset(self):
        self.site = get_current_site(self.request)
        self.long_slug = self.kwargs['blog__slug']
        self.article = self.model.objects.filter(
            site_domain=self.site.domain,
            blog__slug=self.long_slug,
            slug=self.kwargs['slug'],
            date_available__lte=timezone.now(),
            published=True)
        return self.article
