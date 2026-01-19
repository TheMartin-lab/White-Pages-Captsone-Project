from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .models import Article
from .forms import ArticleForm
from .services import send_approval_notifications

# Public Views
def site_home(request):
    return render(request, 'index.html')

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

@login_required
@user_passes_test(is_editor)
def decline_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('reason', '').strip()
        article.approved = False
        article.approved_by = None
        article.declined_reason = reason
        article.declined_by = request.user
        from django.utils import timezone
        article.declined_at = timezone.now()
        article.save()
        messages.warning(request, f'Article "{article.title}" declined.')
        return redirect('approval_list')
    return redirect('approval_detail', pk=pk)
@login_required
def create_article(request):
    if not request.user.is_journalist():
        raise PermissionDenied("You do not have permission to create articles.")
        
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            # New articles might need approval, defaulting to False in model usually
            article.save()
            messages.success(request, 'Article created successfully and submitted for approval.')
            # Redirect to home or maybe a "My Articles" page if we had one. 
            # For now, redirect to detail page (it might be visible if author or not approved?)
            # Or redirect to home.
            return redirect('home') 
    else:
        form = ArticleForm()
    
    return render(request, 'articles/article_form.html', {'form': form, 'title': 'Create Article'})

@login_required
def edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    
    # Permission Check
    if request.user.is_editor():
        pass # Editor can edit anything
    elif request.user.is_journalist() and article.author == request.user:
        pass # Journalist can edit their own
    else:
        raise PermissionDenied("You do not have permission to edit this article.")
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            # If a journalist edits an approved article, does it need re-approval?
            # For now, let's keep the current status or reset if needed. 
            # Assuming editors edits maintain approval, journalist edits might reset.
            # Let's keep it simple: if journalist edits, it might need re-approval if policy says so.
            # For now, we won't change approval status automatically unless requested.
            article.save()
            messages.success(request, 'Article updated successfully.')
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'articles/article_form.html', {'form': form, 'article': article, 'title': 'Edit Article'})

@login_required
def my_articles(request):
    if not request.user.is_journalist():
        raise PermissionDenied("You do not have permission to view this page.")
    articles = Article.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'articles/my_articles.html', {'articles': articles, 'title': 'My Articles'})
