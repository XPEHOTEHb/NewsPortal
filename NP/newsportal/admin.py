from django.contrib import admin
from .models import Post, Author, Category, Comment, PostCategory, Subscribe

admin.site.register(Category)
# admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(PostCategory)



class PostCategoryInLine(admin.TabularInline):
    model = PostCategory


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('author', 'category', 'dateCreation', 'display_postCategory', 'title', 'text', 'rating')
    fields = ('author', 'category', 'title', 'text', 'rating')
    inlines = [PostCategoryInLine, ]


