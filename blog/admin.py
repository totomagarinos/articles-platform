from django.contrib import admin
from .models import Category, Tag, Article, Comment, Review

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Review)
