from django.urls import path
from .views import register, login_view, logout_view, subscribe_to_author

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('subscribe/<int:author_id>/', subscribe_to_author, name='subscribe_to_author'),
]
