from .models import Category, Tag
from users.models import CustomUser


def search_filters(request):
  return {
    'categories': Category.objects.all(),
    'tags': Tag.objects.all(),
    'authors': CustomUser.objects.filter(role=CustomUser.WRITER),
  }
