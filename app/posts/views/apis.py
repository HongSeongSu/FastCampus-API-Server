import django_filters
from rest_framework import permissions
from rest_framework import viewsets

from ..filters import PostFilter
from ..models import Post
from ..serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # pagination_class = Pagination10
    # filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    # filter_class = PostFilter
