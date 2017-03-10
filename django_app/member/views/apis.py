from rest_auth.registration.views import (
    RegisterView as RestSignupView
)
from rest_auth.views import (
    LoginView as RestLoginView,
    LogoutView as RestLogoutView,
    UserDetailsView as RestUserDetailView,
)

from member.serializers import SignupSerializer


class LoginView(RestLoginView):
    pass


class LogoutView(RestLogoutView):
    pass


class SignupView(RestSignupView):
    serializer_class = SignupSerializer


class UserDetailView(RestUserDetailView):
    pass
