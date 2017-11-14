import django_filters
from rest_framework import permissions
from rest_framework import viewsets

from post.filters import PostFilter
from post.models import Post
from post.serializers import PostSerializer
from utils.rest.pagination import Pagination10


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()[:20]
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # pagination_class = Pagination10
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = PostFilter
