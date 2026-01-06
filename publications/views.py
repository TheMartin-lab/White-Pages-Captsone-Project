from rest_framework import viewsets, permissions
from .models import Publisher
from .serializers import PublisherSerializer
from users.permissions import IsEditor

class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsEditor()]
        return super().get_permissions()

    def perform_create(self, serializer):
        publisher = serializer.save()
        publisher.editors.add(self.request.user)
