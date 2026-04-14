from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    ArticleListView,
    ArticleDetailView,
    ArticleCreateView,
    MyArticlesView,
    ArticleUpdateView,
    ArticleDeleteView,
    category_search,
    submit_for_review,
    PendingArticlesView,
    ReviewArticleView,
    tag_search,
    toggle_like,
)

urlpatterns = [
    path("", ArticleListView.as_view(), name="article_list"),
    path("article/create/", ArticleCreateView.as_view(), name="article_create"),
    path(
        "article/delete/<slug:slug>/",
        ArticleDeleteView.as_view(),
        name="article_delete",
    ),
    path("article/<slug:slug>/submit/", submit_for_review, name="submit_for_review"),
    path("article/<slug:slug>/like/", toggle_like, name="toggle_like"),
    path("article/<slug:slug>/edit/", ArticleUpdateView.as_view(), name="article_edit"),
    path(
        "article/<slug:slug>/review/",
        ReviewArticleView.as_view(),
        name="review_article",
    ),
    path("article/<slug:slug>/", ArticleDetailView.as_view(), name="article_detail"),
    path("my-articles/", MyArticlesView.as_view(), name="my_articles"),
    path("pending-articles/", PendingArticlesView.as_view(), name="pending_articles"),
    path("api/categories/", category_search, name="category_search"),
    path("api/tags/", tag_search, name="tag_search"),
]
