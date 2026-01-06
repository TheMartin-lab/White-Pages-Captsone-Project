from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from articles.models import Article, Newsletter

class Command(BaseCommand):
    help = 'Setup user roles and permissions'

    def handle(self, *args, **kwargs):
        try:
            article_ct = ContentType.objects.get_for_model(Article)
            newsletter_ct = ContentType.objects.get_for_model(Newsletter)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error getting content types: {e}. Make sure migrations are applied.'))
            return

        roles_permissions = {
            'Reader': {
                'articles': ['view_article'],
                'newsletters': ['view_newsletter'],
            },
            'Journalist': {
                'articles': ['add_article', 'change_article', 'delete_article', 'view_article'],
                'newsletters': ['add_newsletter', 'change_newsletter', 'delete_newsletter', 'view_newsletter'],
            },
            'Editor': {
                'articles': ['change_article', 'delete_article', 'view_article'],
                'newsletters': ['change_newsletter', 'delete_newsletter', 'view_newsletter'],
            }
        }

        for role_name, perms_map in roles_permissions.items():
            group, created = Group.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created group {role_name}'))
            
            # Clear existing permissions to ensure exact match
            group.permissions.clear()

            # Articles permissions
            for codename in perms_map.get('articles', []):
                try:
                    perm = Permission.objects.get(codename=codename, content_type=article_ct)
                    group.permissions.add(perm)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Permission {codename} not found for Article'))

            # Newsletters permissions
            for codename in perms_map.get('newsletters', []):
                try:
                    perm = Permission.objects.get(codename=codename, content_type=newsletter_ct)
                    group.permissions.add(perm)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Permission {codename} not found for Newsletter'))
            
            self.stdout.write(self.style.SUCCESS(f'Updated permissions for {role_name}'))
