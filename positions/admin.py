from django.contrib import admin
from .models        import Category, Position, Subcategory


class CategoryAdmin(admin.ModelAdmin):
    ...


class SubcategoryAdmin(admin.ModelAdmin):
    list_display  = ['id', 'name', 'category']
    search_fields = ['name', 'category__name']
    list_filter   = ['category']
    ordering      = ['name']


@admin.register(Position)
class positionAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'title', 'created_at', 'profile', 'shift',
        'subcategory', 'state', 'city'
    ]

    list_display_links = ('title', 'created_at')

    search_fields = [
        'id', 'title', 'description', 'slug',
        'state', 'city'
    ]

    list_filter = [
        'category', 'profile', 'shift',
        'subcategory', 'state', 'city',
    ]

    list_per_page       = 10
    ordering            = ['-id']
    prepopulated_fields = {"slug": ('title',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)