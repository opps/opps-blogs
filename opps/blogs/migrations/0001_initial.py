# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Migration(SchemaMigration):

    depends_on = (
        ("images", "0001_initial"),
        ("articles", "0001_initial"),
        ("multimedias", "0001_initial"),
    )

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'blogs_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_insert', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['sites.Site'])),
            ('site_iid', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True, max_length=4, null=True, blank=True)),
            ('site_domain', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=100, null=True, blank=True)),
            ('date_available', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, db_index=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=150)),
            ('blog', self.gf('django.db.models.fields.related.ForeignKey')(related_name='categories', to=orm['blogs.Blog'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('long_slug', self.gf('django.db.models.fields.SlugField')(max_length=250)),
            ('show_in_menu', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('group', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='subchannel', null=True, to=orm['blogs.Category'])),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'blogs', ['Category'])

        # Adding unique constraint on 'Category', fields ['site', 'long_slug', 'slug', 'parent']
        db.create_unique(u'blogs_category', ['site_id', 'long_slug', 'slug', 'parent_id'])

        # Adding model 'Blog'
        db.create_table(u'blogs_blog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_insert', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['sites.Site'])),
            ('site_iid', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True, max_length=4, null=True, blank=True)),
            ('site_domain', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=100, null=True, blank=True)),
            ('date_available', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, db_index=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=150)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('main_image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['images.Image'], null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'blogs', ['Blog'])

        # Adding M2M table for field user on 'Blog'
        m2m_table_name = db.shorten_name(u'blogs_blog_user')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('blog', models.ForeignKey(orm[u'blogs.blog'], null=False)),
            ('%s' % (User._meta.module_name), models.ForeignKey(orm["%s.%s" % (User._meta.app_label, User._meta.object_name)], null=False))
        ))
        db.create_unique(m2m_table_name, ['blog_id', '%s_id' % (User._meta.module_name)])

        # Adding model 'BlogPost'
        db.create_table(u'blogs_blogpost', (
            (u'container_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['containers.Container'], unique=True, primary_key=True)),
            ('headline', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('short_title', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('blog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blogs.Blog'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blogs.Category'], null=True, blank=True)),
        ))
        db.send_create_signal(u'blogs', ['BlogPost'])

        # Adding M2M table for field albums on 'BlogPost'
        m2m_table_name = db.shorten_name(u'blogs_blogpost_albums')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('blogpost', models.ForeignKey(orm[u'blogs.blogpost'], null=False)),
            ('album', models.ForeignKey(orm[u'articles.album'], null=False))
        ))
        db.create_unique(m2m_table_name, ['blogpost_id', 'album_id'])

        # Adding model 'BlogLink'
        db.create_table(u'blogs_bloglink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_insert', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['sites.Site'])),
            ('site_iid', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True, max_length=4, null=True, blank=True)),
            ('site_domain', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=100, null=True, blank=True)),
            ('date_available', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, db_index=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('blog', self.gf('django.db.models.fields.related.ForeignKey')(related_name='links', to=orm['blogs.Blog'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'blogs', ['BlogLink'])

        # Adding model 'BlogPostVideo'
        db.create_table(u'blogs_blogpostvideo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('blogpost', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blogs.BlogPost'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['multimedias.Video'], null=True, on_delete=models.SET_NULL, blank=True)),
        ))
        db.send_create_signal(u'blogs', ['BlogPostVideo'])

        # Adding model 'BlogPostAudio'
        db.create_table(u'blogs_blogpostaudio', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('blogpost', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blogs.BlogPost'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('audio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['multimedias.Audio'], null=True, on_delete=models.SET_NULL, blank=True)),
        ))
        db.send_create_signal(u'blogs', ['BlogPostAudio'])


    def backwards(self, orm):
        # Removing unique constraint on 'Category', fields ['site', 'long_slug', 'slug', 'parent']
        db.delete_unique(u'blogs_category', ['site_id', 'long_slug', 'slug', 'parent_id'])

        # Deleting model 'Category'
        db.delete_table(u'blogs_category')

        # Deleting model 'Blog'
        db.delete_table(u'blogs_blog')

        # Removing M2M table for field user on 'Blog'
        db.delete_table(db.shorten_name(u'blogs_blog_user'))

        # Deleting model 'BlogPost'
        db.delete_table(u'blogs_blogpost')

        # Removing M2M table for field albums on 'BlogPost'
        db.delete_table(db.shorten_name(u'blogs_blogpost_albums'))

        # Deleting model 'BlogLink'
        db.delete_table(u'blogs_bloglink')

        # Deleting model 'BlogPostVideo'
        db.delete_table(u'blogs_blogpostvideo')

        # Deleting model 'BlogPostAudio'
        db.delete_table(u'blogs_blogpostaudio')


    models = {
        u'%s.%s' % (User._meta.app_label, User._meta.module_name): {
            'Meta': {'object_name': User.__name__},
        },
        u'articles.album': {
            'Meta': {'object_name': 'Album'},
            u'container_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['containers.Container']", 'unique': 'True', 'primary_key': 'True'}),
            'headline': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'})
        },
        u'articles.post': {
            'Meta': {'object_name': 'Post'},
            'albums': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'post_albums'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['articles.Album']"}),
            u'container_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['containers.Container']", 'unique': 'True', 'primary_key': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'headline': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'related_posts': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'post_relatedposts'", 'to': u"orm['containers.Container']", 'through': u"orm['articles.PostRelated']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'})
        },
        u'articles.postrelated': {
            'Meta': {'ordering': "('order',)", 'object_name': 'PostRelated'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'postrelated_post'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['articles.Post']"}),
            'related': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'postrelated_related'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['containers.Container']"})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'blogs.blog': {
            'Meta': {'object_name': 'Blog'},
            'date_available': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'db_index': 'True'}),
            'date_insert': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['images.Image']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['sites.Site']"}),
            'site_domain': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'site_iid': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['%s.%s']" % (User._meta.app_label, User._meta.object_name)})
        },
        u'blogs.bloglink': {
            'Meta': {'object_name': 'BlogLink'},
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'links'", 'to': u"orm['blogs.Blog']"}),
            'date_available': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'db_index': 'True'}),
            'date_insert': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['sites.Site']"}),
            'site_domain': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'site_iid': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'max_length': '4', 'null': 'True', 'blank': 'True'})
        },
        u'blogs.blogpost': {
            'Meta': {'object_name': 'BlogPost'},
            'albums': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'blogpoast_albums'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['articles.Album']"}),
            'audios': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['multimedias.Audio']", 'null': 'True', 'through': u"orm['blogs.BlogPostAudio']", 'blank': 'True'}),
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blogs.Blog']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blogs.Category']", 'null': 'True', 'blank': 'True'}),
            u'container_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['containers.Container']", 'unique': 'True', 'primary_key': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'headline': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'videos': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['multimedias.Video']", 'null': 'True', 'through': u"orm['blogs.BlogPostVideo']", 'blank': 'True'})
        },
        u'blogs.blogpostaudio': {
            'Meta': {'object_name': 'BlogPostAudio'},
            'audio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['multimedias.Audio']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'blogpost': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blogs.BlogPost']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'blogs.blogpostvideo': {
            'Meta': {'object_name': 'BlogPostVideo'},
            'blogpost': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blogs.BlogPost']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['multimedias.Video']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        u'blogs.category': {
            'Meta': {'ordering': "['name', 'parent__id', 'published']", 'unique_together': "(('site', 'long_slug', 'slug', 'parent'),)", 'object_name': 'Category'},
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'categories'", 'to': u"orm['blogs.Blog']"}),
            'date_available': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'db_index': 'True'}),
            'date_insert': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'long_slug': ('django.db.models.fields.SlugField', [], {'max_length': '250'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'subchannel'", 'null': 'True', 'to': u"orm['blogs.Category']"}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'show_in_menu': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['sites.Site']"}),
            'site_domain': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'site_iid': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'channels.channel': {
            'Meta': {'ordering': "['name', 'parent__id', 'published']", 'unique_together': "(('site', 'long_slug', 'slug', 'parent'),)", 'object_name': 'Channel'},
            'date_available': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'db_index': 'True'}),
            'date_insert': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'homepage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'include_in_main_rss': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'layout': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '250', 'db_index': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'long_slug': ('django.db.models.fields.SlugField', [], {'max_length': '250'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'subchannel'", 'null': 'True', 'to': u"orm['channels.Channel']"}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'show_in_menu': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['sites.Site']"}),
            'site_domain': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'site_iid': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['%s.%s']" % (User._meta.app_label, User._meta.object_name)})
        },
        u'containers.container': {
            'Meta': {'ordering': "['-date_available']", 'unique_together': "(('site', 'child_class', 'channel_long_slug', 'slug'),)", 'object_name': 'Container'},
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['channels.Channel']"}),
            'channel_long_slug': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'channel_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'child_app_label': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'child_class': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'child_module': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'date_available': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'db_index': 'True'}),
            'date_insert': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'hat': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['images.Image']", 'null': 'True', 'through': u"orm['containers.ContainerImage']", 'blank': 'True'}),
            'main_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'containers_container_mainimage'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['images.Image']"}),
            'main_image_caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'polymorphic_containers.container_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'show_on_root_channel': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['sites.Site']"}),
            'site_domain': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'site_iid': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '4000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '140', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['%s.%s']" % (User._meta.app_label, User._meta.object_name)})
        },
        u'containers.containerimage': {
            'Meta': {'ordering': "('order',)", 'object_name': 'ContainerImage'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'container': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['containers.Container']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['images.Image']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'images.image': {
            'Meta': {'object_name': 'Image'},
            'archive': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            'crop_example': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'crop_x1': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'crop_x2': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'crop_y1': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'crop_y2': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'date_available': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'db_index': 'True'}),
            'date_insert': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fit_in': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'flip': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'flop': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'halign': ('django.db.models.fields.CharField', [], {'default': 'False', 'max_length': '6', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['sites.Site']"}),
            'site_domain': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'site_iid': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'smart': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '4000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '140', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['%s.%s']" % (User._meta.app_label, User._meta.object_name)}),
            'valign': ('django.db.models.fields.CharField', [], {'default': 'False', 'max_length': '6', 'null': 'True', 'blank': 'True'})
        },
        u'multimedias.audio': {
            'Meta': {'ordering': "['-date_available', 'title', 'channel_long_slug']", 'object_name': 'Audio'},
            u'container_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['containers.Container']", 'unique': 'True', 'primary_key': 'True'}),
            'headline': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'media_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'posts': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'audio'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['articles.Post']"}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'uolmais': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "u'uolmais_audio'", 'unique': 'True', 'null': 'True', 'to': u"orm['multimedias.MediaHost']"})
        },
        u'multimedias.mediahost': {
            'Meta': {'object_name': 'MediaHost'},
            'embed': ('django.db.models.fields.TextField', [], {'default': "u''"}),
            'host': ('django.db.models.fields.CharField', [], {'default': "u'uolmais'", 'max_length': '16'}),
            'host_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'notuploaded'", 'max_length': '16'}),
            'status_message': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'updated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True'})
        },
        u'multimedias.video': {
            'Meta': {'ordering': "['-date_available', 'title', 'channel_long_slug']", 'object_name': 'Video'},
            u'container_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['containers.Container']", 'unique': 'True', 'primary_key': 'True'}),
            'headline': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'media_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'posts': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'video'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['articles.Post']"}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'uolmais': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "u'uolmais_video'", 'unique': 'True', 'null': 'True', 'to': u"orm['multimedias.MediaHost']"}),
            'youtube': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "u'youtube_video'", 'unique': 'True', 'null': 'True', 'to': u"orm['multimedias.MediaHost']"})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['blogs']