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


class User(AbstractBaseUser, PermissionsMixin):
    date_joined = models.DateTimeField(auto_now_add=True)
    email = models.EmailField('email adress', unique=True)

    is_active    = models.BooleanField(default=True)
    is_staff     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    username = None
    
    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

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
    user         = models.OneToOneField(User, on_delete=models.CASCADE)
    name         = models.CharField(max_length=255, verbose_name=_('Name'))
    cnpj         = models.CharField(max_length=18, validators=[validate_cnpj], unique=True)
    cep          = models.CharField(max_length=100, verbose_name=_('cep'))
    state        = models.CharField(max_length=100, verbose_name=_('State'), default='')
    city         = models.CharField(max_length=100, verbose_name=_('City'), default='')
    neighborhood = models.CharField(max_length=100, verbose_name=_('Neighborhood'), default='')
    street       = models.CharField(max_length=255, verbose_name=_('Street'), default='')
    more         = models.CharField(max_length=255, verbose_name=_('More'), default='')

    def __str__(self):
        return self.name


class Voluntier(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, verbose_name=_('First Name'))
    last_name  = models.CharField(max_length=30, verbose_name=_('Last Name'))
    birth_date = models.DateField(verbose_name=_('Birth date'))
    cpf        = models.CharField(max_length=14, validators=[validate_cpf], unique=True)
    about      = models.CharField(max_length=2500, verbose_name=_('About'), default='')
    linkedin   = models.CharField(max_length=100, default='')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"