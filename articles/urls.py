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
    path('approval/<int:pk>/decline/', web_views.decline_article, name='decline_article'),
     
    # Edit URLs
    path('article/create/', web_views.create_article, name='create_article'),
    path('article/<int:pk>/edit/', web_views.edit_article, name='edit_article'),
    path('my-articles/', web_views.my_articles, name='my_articles'),
]
