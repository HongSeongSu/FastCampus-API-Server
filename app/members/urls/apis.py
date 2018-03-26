from django.conf.urls import url

from ..views.apis import (
    AuthTokenView,
    SignupView,
    UserProfileView,
)

urlpatterns = [
    url(r'^auth-token/$', AuthTokenView.as_view(), name='auth-token'),
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^profile/$', UserProfileView.as_view(), name='profile'),
]
