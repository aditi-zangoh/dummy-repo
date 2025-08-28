from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("posts/", views.PostListView.as_view(), name="post_list"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path(
        "category/<slug:slug>/",
        views.CategoryDetailView.as_view(),
        name="category_detail",
    ),
    path("search/", views.search_posts, name="search"),
    path("comment/<slug:post_slug>/", views.add_comment, name="add_comment"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
