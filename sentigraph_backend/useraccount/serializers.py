from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for user information.
    """

    class Meta:
        model = User
        fields = ("id", "email", "companies", "is_staff", "is_superuser")
        read_only_fields = ("id", "email", "companies", "is_staff", "is_superuser")
