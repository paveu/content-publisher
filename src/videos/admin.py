from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
# Register your models here.
from .models import Video, Category, TaggedItem

class TaggedItemInline(GenericTabularInline):
    model = TaggedItem

class VideoInline(admin.TabularInline):
    model = Video
    max_num = 2

class VideoAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline]
    
    list_display = ["__unicode__", "slug"]
    fields = ['title', 'share_message',
              'embed_code', 'slug', 'order',
              'active',
              'featured', 'free_preview',
              'category']
    prepopulated_fields = {'slug': ["title"]}

    class Meta:
        model = Video

admin.site.register(Video, VideoAdmin)

class CategoryAdmin(admin.ModelAdmin):
    inlines = [VideoInline, TaggedItemInline]

    class Meta:
        model = Category

admin.site.register(Category, CategoryAdmin)
# admin.site.register(TaggedItem)

