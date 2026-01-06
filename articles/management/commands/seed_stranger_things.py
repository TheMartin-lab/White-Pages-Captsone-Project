from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from articles.models import Article
from publications.models import Publisher

class Command(BaseCommand):
    help = "Seed latest articles about fake Stranger Things ending"

    def handle(self, *args, **options):
        User = get_user_model()
        journalist1, _ = User.objects.get_or_create(
            username="reporter1",
            defaults={"role": User.Roles.JOURNALIST, "email": "reporter1@example.com"},
        )
        journalist2, _ = User.objects.get_or_create(
            username="reporter2",
            defaults={"role": User.Roles.JOURNALIST, "email": "reporter2@example.com"},
        )
        if not journalist1.has_usable_password():
            journalist1.set_password("news123!")
            journalist1.save()
        if not journalist2.has_usable_password():
            journalist2.set_password("news123!")
            journalist2.save()
        publisher, _ = Publisher.objects.get_or_create(
            title="Hawkins Gazette",
            defaults={"description": "Local news from Hawkins"},
        )
        publisher.journalists.add(journalist1, journalist2)

        a1, _ = Article.objects.get_or_create(
            title="Stranger Things finale leak is a fake, insiders say",
            defaults={
                "content": "Multiple sources close to production confirm the rumored ending is fabricated. The viral script pages do not match any shooting draft.",
                "author": journalist1,
                "publisher": publisher,
                "approved": True,
            },
        )
        a2, _ = Article.objects.get_or_create(
            title="Fan theory behind ‘fake ending’ trend explained",
            defaults={
                "content": "A detailed breakdown of how the hoax gained traction, including recycled plot points and AI-generated images misattributed to crew.",
                "author": journalist2,
                "publisher": None,
                "approved": True,
            },
        )
        a3, _ = Article.objects.get_or_create(
            title="Why studios confront misinformation around finales",
            defaults={
                "content": "Studios increasingly tackle misinformation campaigns pre-release. Experts outline best practices and community moderation tips.",
                "author": journalist1,
                "publisher": publisher,
                "approved": True,
            },
        )
        self.stdout.write(self.style.SUCCESS("Seeded Stranger Things articles"))
