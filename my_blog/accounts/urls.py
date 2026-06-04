from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('accounts/login/', views.sigin, name="login"),
    path('signup/', views.sign_up, name="signup"),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('add_blog/', views.add_blog, name="add_blog"),
    path('gallery/', views.gallery, name="gallery"),
    path('logout/', views.user_logout, name="logout"),
    path('edit/<int:id>/', views.edit, name="edit"),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('delete/<int:id>/', views.delete, name="delete"),
    path('profile/', views.profile, name="profile"),
    path("search/", views.search, name="search"),
    path("edit_profile/<int:id>/", views.edit_profile, name="edit_profile"),

    # 🔐 PASSWORD RESET (CORRECT NAMES)
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            email_template_name="registration/password_reset_email.html",
        ),
        name="password_reset"
    ),

    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done"
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url=reverse_lazy("login"),
        ),
        name="password_reset_confirm"
    ),

    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete"
    ),
]
