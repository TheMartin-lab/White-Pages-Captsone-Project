from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from articles.views import ArticleViewSet, NewsletterViewSet
from publications.views import PublisherViewSet

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'newsletters', NewsletterViewSet, basename='newsletter')
router.register(r'publishers', PublisherViewSet)

from rest_framework.authtoken import views
from articles import web_views

urlpatterns = [
    path('', web_views.site_home, name='site_home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')),
    path('articles/', include('articles.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', views.obtain_auth_token),
]
