# -*- coding: utf-8 -*-


from opps.containers.search_indexes import ContainerIndex
from haystack.indexes import Indexable

from .models import BlogPost


class BlogPostIndex(ContainerIndex, Indexable):
    """
    Create a class to ability search in django haystack
    """
    def get_model(self):
        return BlogPost

