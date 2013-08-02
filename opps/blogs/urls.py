#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.conf import settings
from django.views.decorators.cache import cache_page

from .views import BlogPostList, BlogPostDetail, BlogList


urlpatterns = patterns(
    '',
    url(r'^(?P<blog__slug>[\w-]+)/authors/$',
        cache_page(settings.OPPS_CACHE_EXPIRE)(BlogList.as_view()),
        name='blogpost-detail'),
    url(r'^(?P<blog__slug>[\w-]+)/(?P<slug>[\w-]+)/$',
        cache_page(settings.OPPS_CACHE_EXPIRE)(BlogPostDetail.as_view()),
        name='blogpost-detail'),
    url(r'^(?P<blog__slug>[\w-]+)/$',
        cache_page(settings.OPPS_CACHE_EXPIRE)(BlogPostList.as_view()),
        name='blogpost-list'),
)
