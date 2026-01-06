from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Article, Newsletter
from .serializers import ArticleSerializer, NewsletterSerializer
from users.permissions import IsJournalist, IsEditor, IsAuthorOrReadOnly
from django.db.models import Q
from .services import send_approval_notifications

class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_editor():
                return Article.objects.all()
            elif user.is_journalist():
                return Article.objects.filter(Q(author=user) | Q(approved=True))
        return Article.objects.filter(approved=True)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            return [IsJournalist()]
        if self.action in ['update', 'partial_update', 'destroy']:
            # Allow Editors to update/delete ANY article
            # Allow Authors (Journalists) to update/delete their OWN articles
            # We can use IsEditor OR IsAuthorOrReadOnly. 
            # Since IsAuthorOrReadOnly denies if not author, we need a custom logic or cleaner permission class.
            # Let's check IsEditor first.
            if self.request.user.is_authenticated and self.request.user.is_editor():
                 return [permissions.IsAuthenticated()]
            return [IsAuthorOrReadOnly()]
        if self.action == 'approve':
            return [IsEditor()]
        return super().get_permissions()

    @action(detail=False, methods=['get'])
    def subscribed(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Get subscribed publishers and journalists
        # Use getattr with default empty queryset to avoid errors if fields don't exist yet or are None
        subscribed_publishers = getattr(user, 'subscriptions_to_publishers', None)
        subscribed_journalists = getattr(user, 'subscriptions_to_journalists', None)
        
        query = Q(approved=True) # Always filter by approved for readers
        
        conditions = Q()
        if subscribed_publishers:
            conditions |= Q(publisher__in=subscribed_publishers.all())
        if subscribed_journalists:
            conditions |= Q(author__in=subscribed_journalists.all())
            
        # If no subscriptions, return empty list or all? Requirement says "subscribed content".
        # If no conditions added (no subscriptions), this returns empty.
        if not conditions:
             return Response([])

        articles = Article.objects.filter(query & conditions)
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        article = self.get_object()
        article.approved = True
        article.approved_by = request.user
        article.save()
        
        send_approval_notifications(article)
        
        return Response({'status': 'article approved'})

class NewsletterViewSet(viewsets.ModelViewSet):
    serializer_class = NewsletterSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Newsletter.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
