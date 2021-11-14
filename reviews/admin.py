from django.contrib import admin

from .models import Category, Genre, Title, User

admin.site.register(User)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
