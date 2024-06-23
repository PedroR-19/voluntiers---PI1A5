from django.contrib import admin
from .models import Category, Vacancy, Subcategory, Day


class CategoryAdmin(admin.ModelAdmin):
    ...


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category']
    search_fields = ['name', 'category__name']
    list_filter = ['category']
    ordering = ['name']


class DayAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'title', 'created_at', 'profile', 'shift',
        'subcategory', 'country', 'state', 'city', 'logradouro'
    ]
    list_display_links = ('title', 'created_at')
    search_fields = [
        'id', 'title', 'description', 'slug', 'requirements',
        'country', 'state', 'city', 'logradouro'
    ]
    list_filter = [
        'category', 'profile', 'requirements_is_html', 'shift',
        'subcategory', 'country', 'state', 'city', 'days'
    ]
    list_per_page = 10
    ordering = ['-id']
    prepopulated_fields = {"slug": ('title',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Day, DayAdmin)
