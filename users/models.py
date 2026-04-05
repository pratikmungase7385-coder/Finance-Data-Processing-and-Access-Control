"""
Users app models.
Custom User model extending AbstractBaseUser with role-based access.
"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class Role(models.TextChoices):
    VIEWER = 'viewer', 'Viewer'
    ANALYST = 'analyst', 'Analyst'
    ADMIN = 'admin', 'Admin'


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', Role.ADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model using email as the unique identifier.
    Roles: viewer, analyst, admin
    """
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.VIEWER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Required for Django admin
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        db_table = 'users'
        ordering = ['-date_joined']

    def __str__(self):
        return f'{self.full_name} ({self.email}) - {self.role}'

    # ---- Role helpers ----
    @property
    def is_admin(self):
        return self.role == Role.ADMIN

    @property
    def is_analyst(self):
        return self.role == Role.ANALYST

    @property
    def is_viewer(self):
        return self.role == Role.VIEWER

    @property
    def can_write(self):
        """Only admins can create/update/delete records."""
        return self.role == Role.ADMIN

    @property
    def can_read_insights(self):
        """Analysts and admins can access insights/dashboard."""
        return self.role in (Role.ANALYST, Role.ADMIN)
