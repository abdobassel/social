from django.contrib import admin

from .models import Gallery, Post


class GalleryAdmin(admin.ModelAdmin):
    list_display = ["post", "is_active", "timestamp"]


class PostAdmin(admin.ModelAdmin):
    list_display = ["truncated_content", "user", "timestamp"]

    def truncated_content(self, obj):
        """
        1. Split the content into words
        2. Take the first three words and join them back into string
        3. If there are more than three words, add an ellipsis (...) to indicate truncation
        """
        words = obj.content.split()
        short_content = " ".join(words[:5])
        if len(words) > 5:
            short_content += " ..."
        return short_content

    truncated_content.short_description = "Truncated Content"


admin.site.register(Post, PostAdmin)
admin.site.register(Gallery, GalleryAdmin)
