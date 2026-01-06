from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model supporting multiple roles (Reader, Journalist, Editor).
    
    Attributes:
        role (str): The user's role in the system.
        bio (str): Short biography for the user profile.
        subscriptions_to_publishers (ManyToManyField): Publishers the user follows (Reader only).
        subscriptions_to_journalists (ManyToManyField): Journalists the user follows (Reader only).
    """
    class Roles(models.TextChoices):
        READER = 'READER', 'Reader'
        JOURNALIST = 'JOURNALIST', 'Journalist'
        EDITOR = 'EDITOR', 'Editor'

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.READER)
    bio = models.TextField(blank=True)
    
    # Reader fields
    subscriptions_to_publishers = models.ManyToManyField('publications.Publisher', blank=True, related_name='subscribers')
    subscriptions_to_journalists = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='journalist_subscribers')

    def is_editor(self):
        return self.role == self.Roles.EDITOR

    def is_journalist(self):
        return self.role == self.Roles.JOURNALIST

    def is_reader(self):
        return self.role == self.Roles.READER
    
    def save(self, *args, **kwargs):
        # Enforce role-based field cleanup if needed
        super().save(*args, **kwargs)
        # Note: M2M fields are saved after the instance is saved, so clearing them here might be tricky 
        # if done purely in save() without signal or view logic. 
        # However, we can enforce logic in views.
