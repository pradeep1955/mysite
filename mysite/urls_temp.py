import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path
from django.views.static import serve

from users import views as user_views

urlpatterns = [
    path("", include("home.urls")),
    path("contacts/", include("myapp.urls")),
    path("polls/", include("polls.urls")),
    path("ads/", include("ads.urls")),
    path("blog/", include("blog.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    re_path(r"^oauth/", include("social_django.urls", namespace="social")),
    path("register/", user_views.register, name="register"),
    path("profile/", user_views.profile, name="profile"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
urlpatterns += [
    re_path(
        r"^site/(?P<path>.*)$",
        serve,
        {
            "document_root": os.path.join(BASE_DIR, "site"),
            "show_indexes": True,
        },
        name="site_path",
    ),
]

urlpatterns += [
    path(
        "favicon.ico",
        serve,
        {
            "path": "favicon.ico",
            "document_root": os.path.join(BASE_DIR, "home/static"),
        },
    ),
]

try:
    from . import github_settings

    social_login = "registration/login_social.html"
    urlpatterns.insert(
        0,
        path(
            "accounts/login/",
            auth_views.LoginView.as_view(template_name=social_login),
        ),
    )
    print("Using", social_login, "as the login template")
except Exception:
    print("Using registration/login.html as the login template")
