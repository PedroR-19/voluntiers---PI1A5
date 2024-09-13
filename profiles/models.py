from django.utils.translation   import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db                  import models

from .validators import validate_cpf, validate_cnpj


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):  # Adiciona PermissionsMixin
    email       = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    is_active    = models.BooleanField(default=True)
    is_staff     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return self.is_superuser


class Institution(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    cnpj = models.CharField(max_length=18, validators=[validate_cnpj])

    def __str__(self):
        return self.name


class Voluntier(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, verbose_name=_('First Name'))  # Corrigido aqui
    last_name  = models.CharField(max_length=30, verbose_name=_('Last Name'))  # Corrigido aqui
    birth_date = models.DateField(verbose_name=_('Birth date'))
    cpf        = models.CharField(max_length=14, validators=[validate_cpf])

    def __str__(self):
        return f"{self.first_name} {self.last_name}"