from django.db import models
from django.conf import settings

class Publisher(models.Model):
    """
    Represents a media publisher or organization.
    
    Attributes:
        title (str): Name of the publisher.
        description (str): Description of the publisher.
        editors (ManyToManyField): Editors associated with this publisher.
        journalists (ManyToManyField): Journalists working for this publisher.
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    editors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='publisher_editors', blank=True)
    journalists = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='publisher_journalists', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
