# -*- coding: utf-8 -*-
from django import template
from django.utils import timezone

from opps.blogs.models import Blog

register = template.Library()


@register.simple_tag()
def get_blogs(type='blog'):

    blogs = Blog.objects.filter(
        type=type,
        published=True,
        date_available__lte=timezone.now(),
    )

    return blogs
