from django.db import models

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