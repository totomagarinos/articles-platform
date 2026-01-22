from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article

class ArticleListView(ListView):
  model = Article
  template_name = 'blog/article_list.html'
  context_object_name = 'articles'

  def get_queryset(self):
    return Article.objects.filter(status=Article.PUBLISHED)


class ArticleDetailView(DetailView):
  model = Article
  template_name = 'blog/article_detail.html'
  context_object_name = 'article'