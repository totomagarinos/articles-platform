from django.test import TestCase, Client
from django.urls import reverse
from users.models import CustomUser
from .models import Article, Category, Tag

class ArticleFormTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='writer',
            password='password',
            role=CustomUser.WRITER
        )
        self.client = Client()
        self.client.force_login(self.user)
        
        self.category = Category.objects.create(name="Tech", slug="tech")
        self.tag = Tag.objects.create(name="Python", slug="python")

    def test_create_article_button_text(self):
        url = reverse('article_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Check for the button with specific text
        self.assertContains(response, '<button type="submit">Crear</button>')

    def test_edit_article_button_text(self):
        article = Article.objects.create(
            title="My Article",
            slug="my-article",
            content="Content here",
            author=self.user,
            category=self.category,
            status=Article.DRAFT
        )
        article.tags.add(self.tag)
        
        url = reverse('article_edit', kwargs={'slug': article.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Check for the button with specific text
        self.assertContains(response, '<button type="submit">Editar</button>')
