from django.db import models
from django.conf import settings

class Publisher(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    editors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='publisher_editors', blank=True)
    journalists = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='publisher_journalists', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
