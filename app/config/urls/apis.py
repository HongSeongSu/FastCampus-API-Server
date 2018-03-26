from django.conf.urls import url, include
from django.urls import path

from members.urls import apis as apis_member
from posts.urls import apis as apis_post

urlpatterns = [
    path('members/', include(apis_member)),
    path('posts/', include(apis_post)),
]
