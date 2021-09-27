from haystack import indexes
from .models import Portfolio, AlmaMater


class PortfolioIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Portfolio

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(deleted=False)


class AlmaMaterIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return AlmaMater

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(deleted=False, author=None)