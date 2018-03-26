from django.conf.urls import url, include

from members.urls import apis as apis_member
from posts.urls import apis as apis_post

urlpatterns = [
    url(r'^members/', include(apis_member)),
    url(r'^posts/', include(apis_post)),
]
