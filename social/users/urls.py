from django.urls import path, re_path

from social.users.views import (
    CustomProviderAuthView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    LogoutView,
)

urlpatterns = [
    path("jwt/create/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair_view"),  # api/token/
    path("jwt/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh_view"),  # api/token/refresh/
    path("jwt/verify/", CustomTokenVerifyView.as_view(), name="token_verify_view"),  # api/token/verify/
    path("logout/", LogoutView.as_view(), name="logout_view"),  # api/logout/
    re_path(r"^o/(?P<provider>\S+)/$", CustomProviderAuthView.as_view(), name="provider-auth"),
]
