from django.conf.urls import url, include

from member.urls import apis

urlpatterns = [
    url(r'^member/', include(apis)),
]
