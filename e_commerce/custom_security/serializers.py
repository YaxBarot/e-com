from rest_framework import serializers
from .models import AuthTokens, AdminAuthTokens


class AuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthTokens
        fields = "__all__"


class AdminAuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminAuthTokens
        fields = "__all__"
