from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Article
from .services import send_approval_notifications

# Public Views
def site_home(request):
    return render(request, 'home.html')

def home(request):
    articles = Article.objects.filter(approved=True).order_by('-created_at')
    return render(request, 'articles/home.html', {'articles': articles, 'title': 'All News'})

def independent_feed(request):
    articles = Article.objects.filter(approved=True, publisher__isnull=True).order_by('-created_at')
    return render(request, 'articles/home.html', {'articles': articles, 'title': 'Independent Journalism'})

def publisher_feed(request):
    articles = Article.objects.filter(approved=True, publisher__isnull=False).order_by('-created_at')
    return render(request, 'articles/home.html', {'articles': articles, 'title': 'Publisher News'})

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk, approved=True)
    return render(request, 'articles/article_detail.html', {'article': article})

# Editor Views
def is_editor(user):
    return user.is_authenticated and user.is_editor()

@login_required
@user_passes_test(is_editor)
def approval_list(request):
    articles = Article.objects.filter(approved=False)
    return render(request, 'articles/approval_list.html', {'articles': articles})

@login_required
@user_passes_test(is_editor)
def approval_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'articles/approval_detail.html', {'article': article})

@login_required
@user_passes_test(is_editor)
def approve_article(request, pk):
    if request.method == 'POST':
        article = get_object_or_404(Article, pk=pk)
        article.approved = True
        article.approved_by = request.user
        article.save()
        
        # Approval logic: Email + Twitter integration
        try:
            send_approval_notifications(article)
            messages.success(request, f'Article "{article.title}" approved and notifications sent.')
        except Exception as e:
            messages.warning(request, f'Article approved but notification failed: {str(e)}')
            
        return redirect('approval_list')
    return redirect('approval_detail', pk=pk)
