from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Category, Comment, Post, Profile, Tag


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "is_active", "post_count", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["created_at", "updated_at"]

    def post_count(self, obj):
        return obj.posts.count()

    post_count.short_description = "Posts"  # type: ignore


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "post_count", "created_at"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["created_at", "updated_at"]

    def post_count(self, obj):
        return obj.posts.count()

    post_count.short_description = "Posts"  # type: ignore


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "category",
        "is_published",
        "published_at",
        "views_count",
        "created_at",
    ]
    list_filter = ["is_published", "category", "created_at", "published_at", "tags"]
    search_fields = ["title", "content", "excerpt"]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ["created_at", "updated_at", "views_count", "published_at"]
    filter_horizontal = ["tags"]

    fieldsets = (
        ("Basic Information", {"fields": ("title", "slug", "author", "category")}),
        ("Content", {"fields": ("excerpt", "content", "featured_image")}),
        ("Publishing", {"fields": ("is_published", "published_at", "tags")}),
        ("Statistics", {"fields": ("views_count",), "classes": ("collapse",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("author", "category")
            .prefetch_related("tags")
        )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["post", "author", "is_approved", "created_at", "comment_preview"]
    list_filter = ["is_approved", "created_at"]
    search_fields = ["content", "author__username", "post__title"]
    readonly_fields = ["created_at", "updated_at"]

    def comment_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    comment_preview.short_description = "Preview"  # type: ignore

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("author", "post")


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
