from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Article
from users.models import CustomUser
from .forms import CommentForm, ArticleCreateForm
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class ArticleListView(ListView):
    model = Article
    template_name = "blog/article_list.html"
    context_object_name = "articles"

    def get_queryset(self):
        return Article.objects.filter(status=Article.PUBLISHED)


class ArticleDetailView(FormMixin, DetailView):
    model = Article
    template_name = "blog/article_detail.html"
    context_object_name = "article"
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        return context

    def get_success_url(self):
        return reverse("article_detail", kwargs={"slug": self.object.slug})

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
        return reverse("article_detail", kwargs={"slug": self.object.slug})


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

    def get_success_url(self):
        return reverse("article_detail", kwargs={"slug": self.object.slug})


class MyArticlesView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "blog/my_articles.html"
    context_object_name = "articles"

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user).order_by("-created_at")
