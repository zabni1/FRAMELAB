from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Language, Technology, TechnologyDetail



@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'photo', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('id', 'name',)

    @admin.display(description='upload photo')
    def upload_photo(self, Language):
        if Language.photo:
            return mark_safe(f'<img src="{Language.photo.url}" width=40 height=40>')
        return 'Нема'

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'slug', 'category', 'lang', 'file')
    prepopulated_fields = {'slug': ('name',)}
    list_display_links = ('id', 'name',)
    search_fields = ('id', 'name',)
    list_per_page = 10
    ordering = ('id', 'lang')
    list_editable = ('description',)



@admin.register(TechnologyDetail)
class TechnologyDetailyAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'photo', 'description', 'tech')
    search_fields = ('id', 'name',)
    list_filter = ('tech',)
    list_per_page = 10

    @admin.display(description='upload photo')
    def upload_photo(self, TechnologyDetail):
        if TechnologyDetail.photo:
            return mark_safe(f'<img src="{TechnologyDetail.photo.url}" width=40 height=40>')
        return 'Нема'



