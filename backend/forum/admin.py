from django.contrib import admin
from .models import Category, Thread, Reply

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display  = ('title', 'category', 'symbol', 'author', 'created_at', 'is_pinned', 'is_locked')
    list_filter   = ('is_pinned', 'is_locked', 'category')
    search_fields = ('title', 'symbol', 'author__username')

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('thread', 'author', 'created_at')
