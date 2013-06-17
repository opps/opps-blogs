#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from opps.core.admin import apply_opps_rules
from opps.contrib.multisite.admin import AdminViewPermission
from opps.containers.admin import ContainerSourceInline, ContainerImageInline
from opps.containers.admin import ContainerAdmin

from .forms import BlogPostAdminForm
from .models import Blog, BlogPost


@apply_opps_rules('blogs')
class BlogPostAdmin(ContainerAdmin, AdminViewPermission):
    form = BlogPostAdminForm
    inlines = [ContainerImageInline, ContainerSourceInline]
    raw_id_fields = ['main_image', 'channel', 'albums']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'title', 'slug', 'get_http_absolute_url',
                       'short_url')}),
        (_(u'Content'), {
            'fields': ('hat', 'short_title', 'headline', 'content',
                       ('main_image', 'image_thumb'), 'tags')}),
        (_(u'Relationships'), {
            'fields': ('channel', 'albums',)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available',
                       'show_on_root_channel', 'in_containerboxes')}),
    )


class BlogAdmin(admin.ModelAdmin):
    filter_horizontal = ('user',)

admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Blog, BlogAdmin)
