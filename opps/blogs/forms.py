#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms

from .models import BlogPost

from opps.core.widgets import OppsEditor


class BlogPostAdminForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        widgets = {'content': OppsEditor()}
