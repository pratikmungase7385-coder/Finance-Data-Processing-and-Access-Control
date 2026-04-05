
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Role


class UserSerializer(serializers.ModelSerializer):
    """Read serializer for user data (no password)."""

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'role', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer for creating a new user (admin only)."""
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 'role', 'is_active']

    def validate_role(self, value):
        valid_roles = [r.value for r in Role]
        if value not in valid_roles:
            raise serializers.ValidationError(f'Role must be one of: {", ".join(valid_roles)}')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    """Serializer for updating user details (admin only)."""

    class Meta:
        model = User
        fields = ['full_name', 'role', 'is_active']

    def validate_role(self, value):
        valid_roles = [r.value for r in Role]
        if value not in valid_roles:
            raise serializers.ValidationError(f'Role must be one of: {", ".join(valid_roles)}')
        return value


class LoginSerializer(serializers.Serializer):
    """Serializer for login with email + password."""
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials.')
        if not user.is_active:
            raise serializers.ValidationError('This account is inactive.')
        data['user'] = user
        return data
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password']  

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.role = 'viewer' 
        user.save()
        return user