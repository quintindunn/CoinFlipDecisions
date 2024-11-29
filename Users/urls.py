from django.urls import path
from .views import sign_up_with_google, google_oauth_handler, LoginView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', LoginView.as_view(), name="users-login"),
    path('logout/', auth_views.logout_then_login, name="users-logout"),
    path('signup/google/', sign_up_with_google),
    path('google/oauth/', google_oauth_handler, name="google-redirect-uri-0"),
]
