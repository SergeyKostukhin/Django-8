from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'header': ['icontains'],
            'category': ['exact'],
            'date': ['gt'],
        }