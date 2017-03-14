from rest_auth.registration.serializers import RegisterSerializer

try:
    from allauth.account import app_settings as allauth_settings
    from allauth.utils import (email_address_exists,
                               get_username_max_length)
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
except ImportError:
    raise ImportError("allauth needs to be added to INSTALLED_APPS.")
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'first_name',
            'last_name',
            'email',
        )


class SignupSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=30, required=False)

    def get_cleaned_data(self):
        ret = super().get_cleaned_data()
        ret['first_name'] = self.validated_data.get('first_name', '')
        ret['last_name'] = self.validated_data.get('last_name', '')
        ret['email'] = self.validated_data.get('email', '')
        return ret
