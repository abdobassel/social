from django.contrib import admin

from .models import Profile


class UserProfilesAdmin(admin.ModelAdmin):
    list_display = ["get_username"]
    list_display_links = ["get_username"]
    list_filter = ["user"]
    search_fields = ["user__username", "phone_number"]
    list_per_page = 10

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.user = None

    @staticmethod
    def get_username(obj):
        return obj.user.username


admin.site.register(Profile, UserProfilesAdmin)
