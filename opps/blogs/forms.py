#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms

from .models import BlogPost

from redactor.widgets import RedactorEditor


class BlogPostAdminForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        widgets = {'content': RedactorEditor()}
