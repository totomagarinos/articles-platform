from django import forms
from django.utils.text import slugify
from .models import Comment, Article, Review


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        labels = {"content": ""}
        widgets = {
            "content": forms.Textarea(
                attrs={"placeholder": "Escribe tu comentario...", "rows": 4}
            )
        }


class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content", "image", "category"]
        widgets = {
            "content": forms.Textarea(attrs={"placeholder": "Escribe el contenido de tu artículo..."}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.slug:
            instance.slug = slugify(instance.title)
        if commit:
            instance.save()
        return instance


class ReviewArticleForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["decision", "comments"]
        widgets = {
            "decision": forms.RadioSelect(),
            "comments": forms.Textarea(
                attrs={"placeholder": "Feedback para el autor...", "rows": 4}
            ),
        }
