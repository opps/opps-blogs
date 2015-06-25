#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from opps.core.admin import (apply_opps_rules, PublishableAdmin,
                             NotUserPublishableAdmin)
from opps.contrib.multisite.admin import AdminViewPermission

from opps.containers.admin import ContainerAdmin
from opps.channels.models import Channel

from .forms import BlogPostAdminForm
from .models import (
    Category, Blog, BlogRelated, BlogChannelRelated, BlogPost, BlogPostRelated,
    BlogPostAudio, BlogPostVideo, BlogLink, )

from .conf import settings


class BlogAdminPermission(AdminViewPermission):

    def queryset(self, request):
        queryset = super(BlogAdminPermission, self).queryset(request)
        if request.user.is_superuser:
            return queryset

        blogs = Blog.objects.filter(user=request.user)
        if blogs.exists():
            return queryset.filter(blog__in=blogs)
        return queryset.none()

    def get_form(self, request, obj=None, **kwargs):
        form = super(BlogAdminPermission, self).get_form(request, obj,
                                                         **kwargs)
        if request.user.is_superuser:
            return form

        blogs = Blog.objects.filter(user=request.user)
        if blogs.exists():
            form.base_fields['blog'].choices = (
                (b.id, b.name) for b in blogs
            )
        return form

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True

        blogpermission = Blog.objects.filter(user=request.user)
        if len(blogpermission) == 0:
            return False
        return True


@apply_opps_rules('blogs')
class BlogPostRelatedInline(admin.TabularInline):
    model = BlogPostRelated
    fk_name = 'blogpost'
    raw_id_fields = ['related']
    actions = None
    ordering = ('order',)
    extra = 1
    classes = ('collapse',)
    verbose_name = _('Related blog post')
    verbose_name_plural = _('Related blog posts')
    sortable_field_name = 'order'


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
class BlogPostAdmin(ContainerAdmin, BlogAdminPermission):
    form = BlogPostAdminForm
    inlines = [BlogPostRelatedInline]
    list_display = ['title', 'category', 'published', 'get_http_absolute_url']
    raw_id_fields = ['main_image', 'channel', 'albums', 'category']

    fieldsets = (
        (_('Identification'), {
            'fields': ('blog', 'site', 'title', 'slug',
                       'get_http_absolute_url', 'short_url')}),
        (_('Content'), {
            'fields': ('hat', 'short_title', 'headline', 'content',
                       ('main_image', 'image_thumb'),
                       'source', 'tags', 'accept_comments')}),
        (_('Relationships'), {
            'fields': ('albums', 'category')}),
        (_('Publication'), {
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
            raise Channel.DoesNotExist(_('%s channel is not created') % (
                settings.OPPS_BLOGS_CHANNEL)
            )

        super(BlogPostAdmin, self).save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=True):
        if request.user.is_superuser:
            return True
        return super(BlogPostAdmin, self).has_change_permission(request, obj)

    def get_list_filter(self, request):
        list_filter = super(BlogPostAdmin, self).list_filter
        return list_filter + ['category', 'blog']


@apply_opps_rules('blogs')
class BlogRelatedInline(admin.TabularInline):
    model = BlogRelated
    fk_name = 'blog'
    raw_id_fields = ['related']
    actions = None
    ordering = ('order',)
    extra = 1
    classes = ('collapse',)
    verbose_name = _('Related blog')
    verbose_name_plural = _('Related blogs')
    sortable_field_name = 'order'


@apply_opps_rules('blogs')
class BlogChannelRelatedInline(admin.TabularInline):
    model = BlogChannelRelated
    fk_name = 'blog'
    raw_id_fields = ['related']
    actions = None
    ordering = ('order',)
    extra = 1
    classes = ('collapse',)
    verbose_name = _('Related channel')
    verbose_name_plural = _('Related channels')
    sortable_field_name = 'order'


@apply_opps_rules('blogs')
class BlogAdmin(NotUserPublishableAdmin):
    prepopulated_fields = {"slug": ["name"]}
    filter_horizontal = ('user',)
    inlines = [BlogRelatedInline, BlogChannelRelatedInline]
    raw_id_fields = ['main_image', ]
    search_fields = ('name',)
    list_display = ['name', 'site', 'published']
    list_filter = ['date_available', 'published']

    fieldsets = (
        (_('Identification'), {
            'fields': ('site', 'type', 'name', 'slug', 'description',
                       'layout_mode', 'main_image', 'user')}),
        (_('Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available', 'external')}),
    )

    def has_change_permission(self, request, obj=True):
        if request.user.is_superuser:
            return True
        return super(BlogAdmin, self).has_change_permission(request, obj)


@apply_opps_rules('blogs')
class CategoryAdmin(PublishableAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'parent', 'site', 'blog', 'date_available',
                    'order', 'published']
    list_filter = ['date_available', 'published', 'site', 'parent', 'blog']
    search_fields = ['name']
    exclude = ('long_slug',)
    raw_id_fields = ['parent']

    fieldsets = (
        (_('Identification'), {
            'fields': ('blog', 'site', 'parent', 'name', 'slug', 'order',
                       ('show_in_menu',), 'group')}),
        (_('Publication'), {
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
        if not blogpermission.exists():
            return False
        return True

    def queryset(self, request):
        qs = super(CategoryAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs

        return qs.filter(blog__user=request.user)

    def has_change_permission(self, request, obj=True):
        if request.user.is_superuser:
            return True
        return super(CategoryAdmin, self).has_change_permission(request, obj)


@apply_opps_rules('blogs')
class BlogLinkAdmin(BlogAdminPermission):
    list_display = ['name', 'link', 'published']

    fieldsets = (
        (_('Identification'), {
            'fields': ('blog', 'name', 'link')}),
        (_('Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published',)}),
    )

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return super(BlogLinkAdmin, self).has_change_permission(request, obj)

admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogLink, BlogLinkAdmin)
admin.site.register(Category, CategoryAdmin)
