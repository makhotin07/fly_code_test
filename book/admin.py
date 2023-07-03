from django.contrib import admin
from .models import Author, Book, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'archived', 'comment_count')
    list_filter = ('author', 'archived')
    search_fields = ('title', 'description')
    inlines = [CommentInline]

    def comment_count(self, obj):
        return obj.comments.count()

    comment_count.short_description = 'Comments'


class BookInline(admin.TabularInline):
    model = Book
    extra = 0


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'biography', 'profile_picture', 'book_count')
    search_fields = ('name', 'biography')
    inlines = [BookInline]

    def book_count(self, obj):
        return obj.book_set.count()

    book_count.short_description = 'Books'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'content', 'created_at', 'updated_at')
    list_filter = ('user', 'book')
    search_fields = ('user__username', 'book__title', 'content')
    list_editable = ('content',)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Comment, CommentAdmin)
