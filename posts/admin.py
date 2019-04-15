from django.contrib import admin
from .models import Post, Comment
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    
    list_display = ["user","content",]
    
admin.site.register(Post,PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ["user","post","content"]
admin.site.register(Comment,CommentAdmin)