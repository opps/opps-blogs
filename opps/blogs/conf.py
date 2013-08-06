#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings

from appconf import AppConf


class OppsBlogsConf(AppConf):
    CHANNEL = getattr(settings, 'OPPS_BLOGS_CHANNEL', 'blog')
    class Meta:
        prefix = 'opps_blogs'
