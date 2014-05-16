# -*- coding: utf-8 -*-
from django import template
from django.utils import timezone
from django.shortcuts import get_object_or_404

from opps.blogs.models import Blog
from opps.blogs.models import BlogPost

register = template.Library()


@register.simple_tag()
def get_blogs(type='blog'):

    blogs = Blog.objects.filter(
        type=type,
        published=True,
        date_available__lte=timezone.now(),
    )

    return blogs


@register.assignment_tag
def get_blog_posts(slug):
    blog = get_object_or_404(Blog, slug=slug)
    posts = BlogPost.objects.filter(
                blog=blog,
                date_available__lte=timezone.now()
            )
    return posts