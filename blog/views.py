from django.db.models import Q
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Article, Category, Tag, Review
from users.models import CustomUser
from .forms import CommentForm, ArticleCreateForm, ReviewArticleForm
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import transaction


class ArticleListView(ListView):
    model = Article
    template_name = "blog/article_list.html"
    context_object_name = "articles"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        queryset = Article.objects.filter(status=Article.PUBLISHED)

        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            ).distinct()

        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
            
        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__slug=tag)

        author = self.request.GET.get('author')
        if author:
            queryset = queryset.filter(author__username=author)

        return queryset.distinct()


class ArticleDetailView(FormMixin, DetailView):
    model = Article
    template_name = "blog/article_detail.html"
    context_object_name = "article"
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        article = self.object
        user = self.request.user

        if (user.is_authenticated and user == article.author):
            last_review = Review.objects.filter(article=article).first()

            if last_review:
                context["last_review"] = last_review

        return context

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect(f"/admin/login/?next={request.path}")

        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.article = self.object
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("article_detail", kwargs={"slug": self.object.slug})


class ArticleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Article
    form_class = ArticleCreateForm
    template_name = "blog/article_form.html"

    def test_func(self):
        user = self.request.user
        return user.role == CustomUser.WRITER

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect("article_list")
        else:
            return super().handle_no_permission()

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("my_articles")


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleCreateForm
    template_name = "blog/article_form.html"

    def test_func(self):
        article = self.get_object()

        return article.author == self.request.user and article.status in [
            Article.DRAFT,
            Article.REJECTED,
        ]

    def form_valid(self, form):
        if self.object.status == Article.REJECTED:
            form.instance.status = Article.DRAFT

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("my_articles")


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = "blog/article_confirm_delete.html"

    success_url = reverse_lazy("my_articles")

    def test_func(self):
        article = self.get_object()
        return article.author == self.request.user


class MyArticlesView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Article
    template_name = "blog/my_articles.html"
    context_object_name = "articles"

    def test_func(self):
        user = self.request.user
        return user.role == CustomUser.WRITER

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user).order_by("-created_at")


@login_required
def submit_for_review(request, slug):
    article = get_object_or_404(Article, slug=slug)

    if article.author != request.user:
        return HttpResponseForbidden("No tienes permiso")

    if article.status != Article.DRAFT:
        return HttpResponseForbidden(
            "Solo artículos en borrador, edita tu artículo antes de volver a enviar a revisión."
        )

    article.status = Article.PENDING
    article.save()

    return redirect("my_articles")


class PendingArticlesView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Article
    template_name = "blog/pending_articles.html"
    context_object_name = "articles"

    def test_func(self):
        user = self.request.user
        return user.role == CustomUser.EDITOR

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect("article_list")
        else:
            return super().handle_no_permission()

    def get_queryset(self):
        return Article.objects.filter(status=Article.PENDING).order_by("created_at")


class ReviewArticleView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Review
    form_class = ReviewArticleForm
    template_name = "blog/review_article.html"

    success_url = reverse_lazy("pending_articles")

    def test_func(self):
        user = self.request.user
        return user.role == CustomUser.EDITOR

    def get_article(self):
        if not hasattr(self, "_article"):
            self._article = get_object_or_404(Article, slug=self.kwargs["slug"])
        return self._article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["article"] = self.get_article()
        return context

    def form_valid(self, form):
        article = self.get_article()

        form.instance.article = article
        form.instance.editor = self.request.user

        with transaction.atomic():
            response = super().form_valid(form)

            if self.object.decision == Review.APPROVED:
                article.status = Article.PUBLISHED
            elif self.object.decision == Review.REJECTED:
                article.status = Article.REJECTED

            article.save()

            return response


@login_required
def toggle_like(request, slug):
    article = get_object_or_404(Article, slug=slug)

    is_liked = article.liked_by.filter(id=request.user.id).exists()

    if is_liked:
        article.liked_by.remove(request.user.id)
        liked = False
    else:
        article.liked_by.add(request.user.id)
        liked = True

    return JsonResponse({"liked": liked, "total_likes": article.liked_by.count()})
