#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from opps.core.admin import apply_opps_rules, PublishableAdmin
from opps.contrib.multisite.admin import AdminViewPermission
from opps.containers.admin import ContainerSourceInline, ContainerImageInline
from opps.containers.admin import ContainerAdmin
from opps.channels.models import Channel

from .forms import BlogPostAdminForm
from .models import (Category, Blog, BlogPost, BlogPostAudio, BlogPostVideo,
                     BlogLink)

from .conf import settings


class AdminBlogPermission(AdminViewPermission):

    def queryset(self, request):
        queryset = super(AdminBlogPermission, self).queryset(request)
        if request.user.is_superuser:
            return queryset

        try:
            blogpermission = Blog.objects.filter(user=request.user)
            return queryset.filter(blog__in=blogpermission)
        except Blog.DoesNotExist:
            return queryset.none()

    def get_form(self, request, obj=None, **kwargs):
        form = super(AdminBlogPermission, self).get_form(request, obj,
                                                         **kwargs)
        if request.user.is_superuser:
            return form
        try:
            blogpermission = Blog.objects.filter(user=request.user)
            form.base_fields['blog'].choices = (
                (b.id, b.name) for b in blogpermission)
        except Blog.DoesNotExist:
            pass
        return form

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True

        blogpermission = Blog.objects.filter(user=request.user)
        if len(blogpermission) == 0:
            return False
        return True

@apply_opps_rules('blogs')
class BlogPostAudioInline(admin.StackedInline):
    model = BlogPostAudio
    raw_id_fields = ['audio']
    actions = None
    extra = 1
    fieldsets = [(None, {
        'classes': ('collapse',),
        'fields': ('audio',)})]


@apply_opps_rules('blogs')
class BlogPostVideoInline(admin.StackedInline):
    model = BlogPostVideo
    raw_id_fields = ['video']
    actions = None
    extra = 1
    fieldsets = [(None, {
        'classes': ('collapse',),
        'fields': ('video',)})]


@apply_opps_rules('blogs')
class BlogPostAdmin(ContainerAdmin, AdminBlogPermission):
    form = BlogPostAdminForm
    inlines = [ContainerImageInline, ContainerSourceInline,
               BlogPostAudioInline, BlogPostVideoInline]
    list_display = ['title', 'published', 'get_http_absolute_url']
    raw_id_fields = ['main_image', 'channel', 'albums', 'category']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('blog', 'site', 'title', 'slug',
                       'get_http_absolute_url', 'short_url')}),
        (_(u'Content'), {
            'fields': ('hat', 'short_title', 'headline', 'content',
                       ('main_image', 'image_thumb'), 'tags')}),
        (_(u'Relationships'), {
            'fields': ('albums', 'category')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available',
                       'show_on_root_channel', 'in_containerboxes')}),
    )

    def save_model(self, request, obj, form, change):
        # TODO: perhaps a get_or_create here
        try:
            obj.channel = Channel.objects.get(
                slug=settings.OPPS_BLOGS_CHANNEL
            )
        except Channel.DoesNotExist:
            raise Channel.DoesNotExist(_(u'%s channel is not created') % (
                settings.OPPS_BLOGS_CHANNEL)
            )

        super(BlogPostAdmin, self).save_model(request, obj, form, change)


@apply_opps_rules('blogs')
class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
    filter_horizontal = ('user',)
    raw_id_fields = ['main_image', ]
    list_display = ['name', 'site', 'published']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'type', 'name', 'slug', 'description',
                       'main_image', 'user')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )


class CategoryAdmin(PublishableAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'parent', 'site', 'date_available',
                    'order', 'published']
    list_filter = ['date_available', 'published', 'site', 'parent']
    search_fields = ['name']
    exclude = ('long_slug',)
    raw_id_fields = ['parent']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('blog', 'site', 'parent', 'name', 'slug',
                       ('show_in_menu',),
                        'group')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super(CategoryAdmin, self).get_form(request, obj,
                                                         **kwargs)
        if request.user.is_superuser:
            return form
        try:
            blogpermission = Blog.objects.filter(user=request.user)
            form.base_fields['blog'].choices = (
                (b.id, b.name) for b in blogpermission)
        except Blog.DoesNotExist:
            pass
        return form

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True

        blogpermission = Blog.objects.filter(user=request.user)
        if len(blogpermission) == 0:
            return False
        return True

    def queryset(self, request):
        qs = super(CategoryAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs

        return qs.filter(blog__user=request.user)


@apply_opps_rules('blogs')
class BlogLinkAdmin(AdminBlogPermission):
    list_display = ['name', 'link', 'published']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('blog', 'name', 'link')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published',)}),
    )


admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogLink, BlogLinkAdmin)
admin.site.register(Category, CategoryAdmin)
