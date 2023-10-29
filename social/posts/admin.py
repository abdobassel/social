from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ["short_content", "user", "timestamp"]

    def short_content(self, obj):
        words = obj.content.split()
        short_content = " ".join(words[:5])
        if len(words) > 5:
            short_content += " ..."
        return short_content

    short_content.short_description = "Short Content"


admin.site.register(Post, PostAdmin)
