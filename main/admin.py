from django.contrib import admin
from .models import Request, Category

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'status', 'created_date')
    list_filter = ('status', 'category')
    search_fields = ('title', 'description')
    readonly_fields = ('created_date',)
