from django.contrib import admin
from .models import Topic

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'email', 'username', 'created_at', 'category', 'slug')
    prepopulated_fields = {'slug': ('title',)}

