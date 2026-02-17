from django.db import models
from users.models import CustomUser

class Category(models.Model):
  name = models.CharField(max_length=40)

  description = models.TextField(max_length=200, blank=True)

  slug = models.SlugField(unique=True)

  class Meta:
    verbose_name_plural = "Categories"

  def __str__(self):
    return self.name


class Tag(models.Model):
  name = models.CharField(max_length=20)

  slug = models.SlugField(unique=True)

  class Meta:
    verbose_name_plural = "Tags"

  def __str__(self):
    return self.name


class Article(models.Model):
  DRAFT = "draft"
  PENDING = "pending"
  PUBLISHED = "published"
  REJECTED = "rejected"

  STATUS_CHOICES = [
    (DRAFT, "Draft"),
    (PENDING, "Under review"),
    (PUBLISHED, "Published"),
    (REJECTED, "Rejected"),
  ]

  title = models.CharField(max_length=100)

  slug = models.SlugField(unique=True)

  content = models.TextField()

  image = models.ImageField(upload_to='articles/', null=True, blank=True)

  author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

  category = models.ForeignKey(Category, on_delete=models.PROTECT)

  tags = models.ManyToManyField(Tag)

  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=DRAFT)

  created_at = models.DateTimeField(auto_now_add=True)

  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    verbose_name = "Article"
    verbose_name_plural = "Articles"
    ordering = ['-created_at']

  def __str__(self):
    return self.title


class Comment(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

  article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')

  content = models.TextField()

  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ['-created_at']

  def __str__(self):
    return f"Comment by {self.user.username} on {self.article.title}"


class Review(models.Model):
  APPROVED = "approved"
  REJECTED = "rejected"

  DECISION_CHOICES = [
    (APPROVED, "Approved"),
    (REJECTED, "Rejected"),
  ]
  
  editor = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)

  article = models.ForeignKey(Article, on_delete=models.CASCADE)

  decision = models.CharField(max_length=20, choices=DECISION_CHOICES)

  comments = models.TextField(blank=True)

  reviewed_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering=['-reviewed_at']

  def __str__(self):
    editor_name = self.editor.username if self.editor else "Editor deleted"
    return f"Review by {editor_name} on {self.article.title}"