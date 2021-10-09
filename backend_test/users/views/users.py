"""Vista usuarios"""

# Django

# Django Rest Framework
from backend_test.users import serializers
from rest_framework.views import APIView
from rest_framework import mixins, viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
# Django rest framework
from rest_framework.permissions import BasePermission


# Serializers
from backend_test.users.serializers import (
    UserLoginSerializer,
    UserModelSerializer,
    UserSignUpSerializer)


# Modes
from backend_test.users.models import User, Employee



class IsAdmin(BasePermission):
    """Allow access only to objects owned by the requesting user"""

    def has_object_permission(self, request, view, obj):
        """Verified user a have a memebership in the obj"""
        return request.user == obj





class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """User view set.

    Maneja el login, signUp y detalle de usuario/empleados.
    """

    queryset = User.objects.filter(is_active=True, is_employed=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    # def get_permissions(self):
    #     """Assign permissions based on action."""
    #     if self.action in ['signup', 'login', 'verify']:
    #         permissions = [AllowAny]
    #     elif self.action in ['retrieve', 'update', 'partial_update']:
    #         permissions = [IsAuthenticated, IsAdmin]
    #     else:
    #         permissions = [IsAuthenticated]
    #     return [p() for p in permissions]

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User sign in."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)


    # @action(detail=True, methods=['put', 'patch'])
    # def profile(self, request, *args, **kwargs):
    #     """Update profile data."""
    #     user = self.get_object()
    #     profile = user.profile
    #     partial = request.method == 'PATCH'
    #     serializer = ProfileModelSerializer(
    #         profile,
    #         data=request.data,
    #         partial=partial
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     data = UserModelSerializer(user).data
    #     return Response(data)

    # def retrieve(self, request, *args, **kwargs):
    #     """Add extra data to the response."""
    #     response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
    #     circles = Circle.objects.filter(
    #         members=request.user,
    #         membership__is_active=True
    #     )
    #     data = {
    #         'user': response.data,
    #         'circles': CircleModelSerializer(circles, many=True).data
    #     }
    #     response.data = data
    #     return response
