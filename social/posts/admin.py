from django.contrib import admin

from .models import Post, PostHashtag


class PostAdmin(admin.ModelAdmin):
    list_display = ["short_content", "user", "timestamp", "views"]

    def short_content(self, obj):
        words = obj.content.split()
        short_content = " ".join(words[:5])
        if len(words) > 5:
            short_content += " ..."
        return short_content

    short_content.short_description = "Short Content"


admin.site.register(Post, PostAdmin)


class PostHashTagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "is_active", "hashtag_time"]


admin.site.register(PostHashtag, PostHashTagAdmin)
