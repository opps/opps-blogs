# -*- coding: utf-8 -*-
from django.contrib.sites.models import get_current_site
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from opps.channels.models import Channel
from opps.views.generic.list import ListView
from opps.contrib.feeds.views import ItemFeed
from opps.views.generic.detail import DetailView
from opps.core.tags.views import TagList
from opps.core.tags.models import Tag

from opps.blogs.models import BlogPost, Blog
from .conf import settings

User = get_user_model()


class BlogMixin(object):

    def get_context_data(self, **kwargs):
        context = super(BlogMixin, self).get_context_data(**kwargs)
        if 'blog__slug' in self.kwargs.keys():
            context['blog'] = get_object_or_404(Blog,
                                                slug=self.kwargs['blog__slug'])
        return context


class BaseListView(BlogMixin, ListView):

    def dispatch(self, request, *args, **kwargs):
        self.site = get_current_site(request)
        self.channel = get_object_or_404(Channel,
                                         slug=settings.OPPS_BLOGS_CHANNEL,
                                         site=self.site)
        return super(BaseListView, self).dispatch(request, *args, **kwargs)

    def get_template_names(self):
        templates = super(BaseListView, self).get_template_names()
        domain_folder = self.get_template_folder()
        blog_slug = self.kwargs['blog__slug']
        templates = [
            '{}/blogs/{}/{}_{}.html'.format(domain_folder,
                                            blog_slug,
                                            self.paginate_suffix,
                                            self.blog_obj.layout_mode),
            '{}/blogs/{}/{}.html'.format(domain_folder,
                                         blog_slug,
                                         self.paginate_suffix),
            '{}/blogs/{}_{}.html'.format(domain_folder,
                                         self.paginate_suffix,
                                         self.blog_obj.layout_mode),
        ] + templates
        return templates


class BlogList(BaseListView):
    model = Blog
    channel_long_slug = []
    paginate_suffix = 'list'

    def get_template_names(self):
        domain_folder = self.get_template_folder()
        templates = ['{}/blogs/blogs.html'.format(domain_folder)]
        return templates

    def get_queryset(self):
        self.long_slug = self.kwargs['channel__long_slug']
        self.blogs = self.model.objects.filter(
            site_domain=self.site.domain,
            date_available__lte=timezone.now(),
            published=True)

        return self.blogs


class BlogUsersList(BaseListView):
    model = Blog
    channel_long_slug = []
    paginate_suffix = 'list'

    def get_template_names(self):
        templates = super(BlogUsersList, self).get_template_names()
        domain_folder = self.get_template_folder()
        templates = ['{}/blogs/{}/authors.html'.format(
            domain_folder,
            self.long_slug,
        ), '{}/blogs/authors.html'.format(
            domain_folder
        )] + templates
        return templates

    def get_queryset(self):
        self.long_slug = self.kwargs['blog__slug']
        self.blogs = self.model.objects.filter(
            site_domain=self.site.domain,
            slug=self.long_slug,
            date_available__lte=timezone.now(),
            published=True)
        if not self.blogs:
            return []
        users_ids = []
        for blog in self.blogs:
            ids = [i.id for i in blog.user.all()]
            users_ids.extend(ids)
        ids = list(set(users_ids))
        return User.objects.filter(pk__in=ids)


class BlogPostList(BaseListView):
    model = BlogPost
    type = "blogs"
    channel_long_slug = []
    paginate_suffix = 'list'
    paginate_by = getattr(settings, 'OPPS_BLOGS_POST_PAGINATE_BY', 15)

    def get_queryset(self):
        self.long_slug = self.kwargs['blog__slug']
        self.blog_obj = get_object_or_404(Blog, slug=self.long_slug)
        self.article = self.model.objects.filter(
            site_domain=self.site.domain,
            blog=self.blog_obj,
            date_available__lte=timezone.now(),
            published=True)

        return self.article


class BlogPostFeed(ItemFeed):
    link = "/rss"

    def item_enclosure_url(self, item):
        if item.main_image:
            if item.main_image.archive:
                i_url = item.main_image.archive.url
            elif item.main_image.archive_link:
                i_url = item.main_image.archive_link
            else:
                i_url = item.main_image.image_url()

            m_url = getattr(settings, 'MEDIA_URL', '')
            if not m_url.startswith('http') and not i_url.startswith('http'):
                i_url = "http://" + item.site_domain + i_url
            return i_url

    def title(self):
        return _("{0}'s news".format(get_current_site(self.request)))

    def description(self):
        return _("Latest news on {0}'s".format(get_current_site(self.request)))

    def get_object(self, request, blog__slug):
        blog = get_object_or_404(Blog, slug=blog__slug)
        self.request = request
        return blog

    def items(self, obj):
        filters = self.build_filters().get('filter', {})
        excludes = self.build_filters().get('exclude', {})

        qs = BlogPost.objects.filter(
            blog=obj,
            date_available__lte=timezone.now(),
            published=True,
            **filters).exclude(
                **excludes
            ).order_by('-date_available')[:40]

        return qs


class BlogPostDateList(BlogPostList):
    def get_queryset(self):
        self.long_slug = self.kwargs['blog__slug']
        self.year = int(self.kwargs['year'])
        self.month = int(self.kwargs['month'])
        self.blog_obj = get_object_or_404(Blog, slug=self.long_slug)

        self.article = self.model.objects.filter(
            site_domain=self.site.domain,
            blog=self.blog_obj,
            date_available__year=self.year,
            date_available__month=self.month,
            published=True)

        return self.article


class CategoryList(BaseListView):
    model = BlogPost
    paginate_suffix = 'list'

    def get_queryset(self):
        self.long_slug = self.kwargs['blog__slug']
        self.category_long_slug = self.kwargs['category_long_slug']
        self.blog_obj = get_object_or_404(Blog, slug=self.long_slug)
        self.article = self.model.objects.filter(
            site_domain=self.site.domain,
            blog=self.blog_obj,
            category__long_slug=self.category_long_slug,
            date_available__lte=timezone.now(),
            published=True)

        return self.article


class BlogPostDetail(DetailView):
    model = BlogPost
    paginate_suffix = 'detail'

    def dispatch(self, request, *args, **kwargs):
        self.site = get_current_site(request)
        self.channel = get_object_or_404(Channel,
                                         slug=settings.OPPS_BLOGS_CHANNEL,
                                         site=self.site)

        return super(BlogPostDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BlogPostDetail, self).get_context_data(**kwargs)

        if 'blog__slug' in self.kwargs.keys():
            context['blog'] = get_object_or_404(Blog,
                                                slug=self.kwargs['blog__slug'])

        return context

    def get_template_names(self):
        domain_folder = self.get_template_folder()
        templates = ['{}/blogs/{}/detail.html'.format(
            domain_folder,
            self.long_slug,
        ), '{}/blogs/detail.html'.format(
            domain_folder
        )]
        return templates

    def get_queryset(self):
        self.long_slug = self.kwargs['blog__slug']
        self.category_long_slug = self.kwargs['category_long_slug']
        lookups = dict(
            site_domain=self.site.domain,
            blog__slug=self.long_slug,
            slug=self.kwargs['slug'],
            published=True,
            date_available__lte=timezone.now()
        )
        if not self.category_long_slug == 'sem-categoria':
            lookups['category__long_slug'] = self.category_long_slug

        self.article = self.model.objects.filter(**lookups)
        return self.article


class BlogTagList(BlogMixin, TagList):
    model = BlogPost

    def get_template_names(self):
        domain_folder = self.get_template_folder()
        blog_slug = self.kwargs.get('blog__slug')
        templates = ['{}/blogs/{}/tags.html'.format(
            domain_folder,
            blog_slug,
        ), '{}/blogs/tags.html'.format(
            domain_folder,
        )]
        return templates

    def get_queryset(self):
        self.site = get_current_site(self.request)
        # without the long_slug, the queryset will cause an error
        self.long_slug = 'tags'
        self.tag = self.kwargs['tag']

        tags = Tag.objects.filter(slug=self.tag).values_list('name') or []
        tags_names = []
        if tags:
            tags_names = [i[0] for i in tags]

        ids = []
        for tag in tags_names:
            result = self.containers = self.model.objects.filter(
                site_domain=self.site,
                tags__contains=tag,
                date_available__lte=timezone.now(),
                published=True,
                blog__slug=self.kwargs['blog__slug'],
            )
            if result.exists():
                ids.extend([i.id for i in result])

        # remove the repeated
        ids = list(set(ids))

        # grab the blogposts
        self.containers = self.model.objects.filter(id__in=ids)

        return self.containers
