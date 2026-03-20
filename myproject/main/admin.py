from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Language, LanguageDetail, LanguageDetailCategory



@admin.register(LanguageDetail)
class LanguageDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'photo', 'slug', 'lang', 'cat')
    prepopulated_fields = {'slug': ('name',)}
    list_display_links = ('id', 'name',)
    search_fields = ('id', 'name',)
    list_filter = ('cat',)
    list_per_page = 10
    ordering = ('id', 'lang', 'cat')
    list_editable = ('description',)


    @admin.display(description='upload photo')
    def upload_photo(self, LanguageDetail):
        if LanguageDetail.photo:
            return mark_safe(f'<img src="{LanguageDetail.photo.url}" width=40 height=40>')
        return 'Нема'

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

@admin.register(LanguageDetailCategory)
class LanguageDetailCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('id', 'name',)



