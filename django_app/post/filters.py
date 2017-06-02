import django_filters

from post.models import Post


class PostFilter(django_filters.rest_framework.FilterSet):
    year = django_filters.NumberFilter(name='created_date', lookup_expr='year')

    class Meta:
        model = Post
        fields = {
            'author': ['exact'],
            'created_date': ['gte', 'lte'],
        }
