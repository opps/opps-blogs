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


class AdminBlogPermission(AdminViewPermission):

    def queryset(self, request):
        queryset = super(AdminBlogPermission, self).queryset(request)
        try:
            blogpermission = Blog.objects.get(user=request.user)
            return queryset.filter(blog=blogpermission)
        except Blog.DoesNotExist:
            return queryset.none()

    def get_form(self, request, obj=None, **kwargs):
        form = super(AdminBlogPermission, self).get_form(request, obj,
                                                         **kwargs)
        import pdb; pdb.set_trace()
        try:
            blogpermission = Blog.objects.filter(user=request.user)
            form.base_fields['blog'].choices = (
                (b.id, b.name) for b in blogpermission)
        except Blog.DoesNotExist:
            pass
        return form

    def has_add_permission(self, request):
        try:
            Blog.objects.filter(user=request.user)
            return True
        except Blog.DoesNotExist:
            return False


@apply_opps_rules('blogs')
class BlogPostAdmin(ContainerAdmin, AdminBlogPermission):
    form = BlogPostAdminForm
    inlines = [ContainerImageInline, ContainerSourceInline]
    raw_id_fields = ['main_image', 'channel', 'albums']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('blog', 'site', 'title', 'slug',
                       'get_http_absolute_url', 'short_url')}),
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
    prepopulated_fields = {"slug": ["name"]}
    filter_horizontal = ('user',)
    raw_id_fields = ['main_image', ]
    list_display = ['name', 'site', 'published']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'name', 'slug', 'description', 'main_image',
                       'user')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )


admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Blog, BlogAdmin)
