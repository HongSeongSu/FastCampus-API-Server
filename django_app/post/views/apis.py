from rest_framework import permissions
from rest_framework import viewsets

from post.models import Post
from post.serializers import PostSerializer
from utils.rest.pagination import Pagination10


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = Pagination10
