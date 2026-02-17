from django import forms
from .models import Comment, Article


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
        fields = ["title", "slug", "content", "image", "category", "tags"]
        widgets = {"tags": forms.CheckboxSelectMultiple(), "content": forms.Textarea()}
