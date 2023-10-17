from django.urls import path

from .views import ProfileDetailView, ProfileListView, UserProfileUpdateView

app_name = "profiles"

urlpatterns = [
    path("list/", ProfileListView.as_view(), name="profile-list"),
    path("<int:pk>/", ProfileDetailView.as_view(), name="profile-detail"),  # Use 'slug' in the URL pattern
    path("<int:pk>/edit/", UserProfileUpdateView.as_view(), name="profile-update"),  # Use 'slug' in the URL pattern
]
