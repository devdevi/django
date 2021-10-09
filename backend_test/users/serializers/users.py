"""User serializers."""
# Django
from backend_test.users.models.employee import Employee
from django.conf import settings
from django.contrib.auth import password_validation, authenticate
from django.core.validators import RegexValidator
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
# Model
from backend_test.users.models import User


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    # profile = ProfileModelSerializer(read_only=True)

    class Meta:
        """Meta class."""

        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',

        )
        read_only_fields = ('employee',)

        depth = 1

class UserLoginSerializer(serializers.Serializer):
    """User login serializer.

    Handle the login request data.
    """
    username = serializers.CharField()
    password = serializers.CharField(min_length=4, max_length=64)

    def validate(self, data):
        """Check credentials."""
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        self.context['user'] = user
        return data

    def create(self, data):
        return self.context['user']



class UserSignUpSerializer(UserModelSerializer):
    """User sign up serializer.

    Handle sign up data validation and user/profile creation.
    """

    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    # Password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)
    class Meta(UserModelSerializer.Meta):
        """Meta class."""

        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'is_admin',
            'password',
            'password_confirmation'
        )

    def validate(self, data):
        """Verify passwords match."""
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Passwords don't match.")
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        """Handle user and profile creation."""
        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_employed=True)
        Employee.objects.create(user=user)
        return user

    def create_admin(self, data):
        """Handle user and profile creation."""
        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_admin=True, is_employed=True)
        Employee.objects.create(user=user)
        return user

