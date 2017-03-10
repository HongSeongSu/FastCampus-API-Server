from django.conf.urls import url, include

from member.urls import apis as apis_member
from post.urls import apis as apis_post

urlpatterns = [
    url(r'^member/', include(apis_member)),
    url(r'^post/', include(apis_post)),
]
