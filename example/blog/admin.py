from django.contrib import admin

from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass
