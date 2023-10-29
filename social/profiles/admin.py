from django.contrib import admin

from .models import Profile


class UserProfilesAdmin(admin.ModelAdmin):
    list_display = ["user", "timestamp", "city"]
    list_filter = ["user"]
    search_fields = ["user__username", "phone_number"]
    list_per_page = 10


admin.site.register(Profile, UserProfilesAdmin)
