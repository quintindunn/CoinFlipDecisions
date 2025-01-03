from django.urls import path
from .views import (
    sign_up_with_google,
    google_oauth_handler,
    set_display_name,
    check_display_name,
    logout_user,
    LoginView,
)


urlpatterns = [
    path("login/", LoginView.as_view(), name="users-login"),
    path("logout/", logout_user, name="users-logout"),
    path("signup/google/", sign_up_with_google),
    path("google/oauth/", google_oauth_handler, name="google-redirect-uri-0"),
    path("account/setdisplayname/", set_display_name, name="set-display-name"),
    path("account/checkdisplayname/", check_display_name, name="check-display-name"),
]
