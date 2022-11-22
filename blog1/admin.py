from django.contrib import admin

from blog1.models import *
# Register your models here.


class TagTublerInline(admin.TabularInline):
    model=Tag

class PostAdmin(admin.ModelAdmin):
    inlines=[TagTublerInline]
    list_display=['title','author','timeStamp','status','section','Main_post','post_views']
    list_editable=['status','section','Main_post']
    search_fields=['title','section']
    list_filter=('category',)
    list_per_page=20
    ordering = ('-post_views',)

class BlogCommentadmin(admin.ModelAdmin):
    # inlines=[TagTublerInline]
    list_display=['post','sno','user','comment',]
    # search_fields=['user']
    list_filter=('user','post',)
    list_per_page=20


# Register your models here.

admin.site.register(Category)
admin.site.register(Post,PostAdmin)
admin.site.register(BlogComment,BlogCommentadmin)
admin.site.register(Tag)