from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,
    ArticleCreateView,
    MyArticlesView,
    ArticleUpdateView,
    ArticleDeleteView,
    submit_for_review,
    PendingArticlesView,
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
    path("article/<slug:slug>/edit/", ArticleUpdateView.as_view(), name="article_edit"),
    path("article/<slug:slug>/", ArticleDetailView.as_view(), name="article_detail"),
    path("my-articles/", MyArticlesView.as_view(), name="my_articles"),
    path("pending-articles/", PendingArticlesView.as_view(), name="pending_articles"),
]
