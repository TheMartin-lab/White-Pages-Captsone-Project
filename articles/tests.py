from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Article, Newsletter
from publications.models import Publisher
from unittest.mock import patch

User = get_user_model()

class ArticleAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create Users
        self.reader = User.objects.create_user(username='reader', password='password', role='READER')
        self.journalist = User.objects.create_user(username='journalist', password='password', role='JOURNALIST')
        self.editor = User.objects.create_user(username='editor', password='password', role='EDITOR')
        self.other_journalist = User.objects.create_user(username='other_journalist', password='password', role='JOURNALIST')
        
        # Create Publisher
        self.publisher = Publisher.objects.create(title='Tech News')
        self.publisher.journalists.add(self.journalist)
        
        # Create Articles
        self.article1 = Article.objects.create(
            title='Article 1', content='Content 1', author=self.journalist, publisher=self.publisher, approved=True
        )
        self.article2 = Article.objects.create(
            title='Article 2', content='Content 2', author=self.other_journalist, approved=True
        )
        self.unapproved_article = Article.objects.create(
            title='Unapproved', content='Draft', author=self.journalist, approved=False
        )

    def test_get_articles_authenticated(self):
        """Test retrieving all approved articles."""
        self.client.force_authenticate(user=self.reader)
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should see approved articles
        
    def test_get_subscribed_articles(self):
        """Test retrieving only subscribed articles."""
        # Reader subscribes to Publisher (Article 1)
        self.reader.subscriptions_to_publishers.add(self.publisher)
        
        self.client.force_authenticate(user=self.reader)
        response = self.client.get('/api/articles/subscribed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.article1.id)
        
        # Reader subscribes to Other Journalist (Article 2)
        self.reader.subscriptions_to_journalists.add(self.other_journalist)
        response = self.client.get('/api/articles/subscribed/')
        self.assertEqual(len(response.data), 2)

    def test_journalist_create_article(self):
        """Test journalist creating an article."""
        self.client.force_authenticate(user=self.journalist)
        data = {'title': 'New Article', 'content': 'New Content', 'publisher': self.publisher.id}
        response = self.client.post('/api/articles/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 4)
        self.assertFalse(Article.objects.get(title='New Article').approved)

    def test_reader_cannot_create_article(self):
        """Test reader cannot create article."""
        self.client.force_authenticate(user=self.reader)
        data = {'title': 'New Article', 'content': 'New Content'}
        response = self.client.post('/api/articles/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_editor_approve_article(self):
        """Test editor approving an article."""
        self.client.force_authenticate(user=self.editor)
        
        # Patch where it is USED, not where it is defined
        with patch('articles.views.send_approval_notifications') as mock_notify:
            response = self.client.post(f'/api/articles/{self.unapproved_article.id}/approve/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.unapproved_article.refresh_from_db()
            self.assertTrue(self.unapproved_article.approved)
            self.assertEqual(self.unapproved_article.approved_by, self.editor)
            mock_notify.assert_called_once()

    def test_journalist_cannot_approve(self):
        """Test journalist cannot approve articles."""
        self.client.force_authenticate(user=self.journalist)
        response = self.client.post(f'/api/articles/{self.unapproved_article.id}/approve/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_article(self):
        """Test delete permissions."""
        # Editor can delete any
        self.client.force_authenticate(user=self.editor)
        response = self.client.delete(f'/api/articles/{self.article1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Journalist can delete own
        self.client.force_authenticate(user=self.other_journalist)
        response = self.client.delete(f'/api/articles/{self.article2.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Journalist cannot delete others (even if approved and visible)
        new_article = Article.objects.create(title='A', content='C', author=self.journalist, approved=True)
        response = self.client.delete(f'/api/articles/{new_article.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class NewsletterAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.journalist = User.objects.create_user(username='journalist', password='password', role='JOURNALIST')
        self.article = Article.objects.create(title='A1', content='C1', author=self.journalist, approved=True)
        self.newsletter = Newsletter.objects.create(title='News 1', author=self.journalist)
        self.newsletter.articles.add(self.article)

    def test_get_newsletters(self):
        self.client.force_authenticate(user=self.journalist)
        response = self.client.get('/api/newsletters/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
