"""
Views for user management and authentication.
"""
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import User
from .serializers import (
    UserSerializer,
    CreateUserSerializer,
    UpdateUserSerializer,
    LoginSerializer,
)
from .permissions import IsAdmin, IsAnyRole


from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(username=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })

        return Response({"detail": "Invalid credentials"}, status=401)

class MeView(APIView):
    """
    GET /api/users/me/
    Returns the currently authenticated user's profile.
    """
    permission_classes = [IsAnyRole]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class UserListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/users/         → Admin: list all users
    POST /api/users/         → Admin: create a user
    """
    queryset = User.objects.all().order_by('-date_joined')
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUserSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/users/<id>/  → Admin: get user by id
    PATCH  /api/users/<id>/  → Admin: update role / status
    DELETE /api/users/<id>/  → Admin: deactivate user (soft delete)
    """
    queryset = User.objects.all()
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return UpdateUserSerializer
        return UserSerializer

    def destroy(self, request, *args, **kwargs):
        """Soft delete: mark user as inactive instead of deleting."""
        user = self.get_object()
        if user == request.user:
            return Response(
                {'detail': 'You cannot deactivate your own account.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.is_active = False
        user.save()
        return Response(
            {'detail': f'User {user.email} has been deactivated.'},
            status=status.HTTP_200_OK,
        )


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer

from rest_framework.permissions import AllowAny



from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .serializers import RegisterSerializer

from rest_framework.permissions import AllowAny

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created"}, status=201)

        return Response(serializer.errors, status=400)