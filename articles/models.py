from django.db import models
from django.conf import settings
from publications.models import Publisher

class Article(models.Model):
    """
    Represents a news article created by a journalist.
    
    Attributes:
        title (str): The headline of the article.
        content (str): The body text of the article.
        image (ImageField): Optional image for the article.
        author (User): The journalist who wrote the article.
        publisher (Publisher): The publisher associated with the article.
        approved (bool): Status of approval by an editor.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authored_articles')
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_articles')
    declined_reason = models.TextField(blank=True)
    declined_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='declined_articles')
    declined_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

class Newsletter(models.Model):
    """
    Represents a newsletter aggregating multiple articles.
    
    Attributes:
        title (str): Title of the newsletter.
        description (str): Brief description.
        author (User): Creator of the newsletter.
        articles (ManyToManyField): Articles included in this newsletter.
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='newsletters')
    articles = models.ManyToManyField(Article, related_name='newsletters')

    def __str__(self):
        return self.title
