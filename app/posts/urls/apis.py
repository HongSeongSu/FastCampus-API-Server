from django.conf.urls import include
from django.conf.urls import url
from rest_framework import routers

from ..views.apis import PostViewSet

router = routers.DefaultRouter()
router.register(r'', PostViewSet)

urlpatterns = [
    url(r'', include(router.urls))
]
