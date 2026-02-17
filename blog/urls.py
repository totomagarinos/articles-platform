from django.urls import path
from .views import ArticleListView, ArticleDetailView, ArticleCreateView, MyArticlesView

urlpatterns = [
  path('', ArticleListView.as_view(), name='article_list'),
  path('my-articles/', MyArticlesView.as_view(), name='my_articles'),
  path("article/create/", ArticleCreateView.as_view(), name="article_create"),
  path('article/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
]
