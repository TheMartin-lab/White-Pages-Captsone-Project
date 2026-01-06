from django.urls import path
from . import web_views

urlpatterns = [
    # Public URLs
    path('', web_views.home, name='home'),
    path('independent/', web_views.independent_feed, name='independent_feed'),
    path('publishers/', web_views.publisher_feed, name='publisher_feed'),
    path('article/<int:pk>/', web_views.article_detail, name='article_detail'),

    # Editor Approval URLs
    path('approval/', web_views.approval_list, name='approval_list'),
    path('approval/<int:pk>/', web_views.approval_detail, name='approval_detail'),
    path('approval/<int:pk>/approve/', web_views.approve_article, name='approve_article'),
]
