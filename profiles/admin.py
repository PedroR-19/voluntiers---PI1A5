from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Institution, Voluntier


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'is_staff', 'is_active')

    list_filter = ('is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),  # Adicione 'groups' e 'user_permissions'
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    readonly_fields = ('date_joined',)  # Defina o campo como somente leitura

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser'),
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')  # Adicione 'groups' e 'user_permissions'


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'cnpj')
    search_fields = ('name', 'cnpj')


@admin.register(Voluntier)
class VoluntierAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'cpf', 'birth_date')
    search_fields = ('first_name', 'last_name', 'cpf')