from django.conf.urls import include
from django.conf.urls import url

from member.views.apis import LoginView, LogoutView, SignupView, UserDetailView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='rest_login'),
    url(r'^logout/$', LogoutView.as_view(), name='rest_logout'),
    url(r'^signup/$', SignupView.as_view(), name='rest_signup'),
    url(r'^profile/$', UserDetailView.as_view(), name='rest_profile'),
]
