from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import messages
from publications.models import Publisher

User = get_user_model()

@login_required
def subscribe_to_author(request, author_id):
    author = get_object_or_404(User, pk=author_id)
    user = request.user
    
    if user.role != User.Roles.READER:
        messages.warning(request, "Only readers can subscribe to authors.")
        return redirect(request.META.get('HTTP_REFERER', 'home'))

    if author == user:
        messages.warning(request, "You cannot subscribe to yourself.")
        return redirect(request.META.get('HTTP_REFERER', 'home'))

    if user.subscriptions_to_journalists.filter(pk=author_id).exists():
        user.subscriptions_to_journalists.remove(author)
        messages.success(request, f"Unsubscribed from {author.username}.")
    else:
        user.subscriptions_to_journalists.add(author)
        messages.success(request, f"Subscribed to {author.username}.")
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')


class RegistrationForm(forms.ModelForm):
    """
    Form for user registration.
    
    Includes fields for basic user info, role selection, and 
    initial subscriptions (for Readers).
    """
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=User.Roles.choices)
    subscriptions_to_publishers = forms.ModelMultipleChoiceField(
        queryset=Publisher.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    subscriptions_to_journalists = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(), # Set in __init__
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure dynamic loading of all journalists
        self.fields['subscriptions_to_journalists'].queryset = User.objects.filter(role=User.Roles.JOURNALIST)
        # We can also refresh publishers if needed, though they change less often
        self.fields['subscriptions_to_publishers'].queryset = Publisher.objects.all()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role']

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Passwords do not match')
        return cleaned

    def save(self, commit=True):
        user = User(
            username=self.cleaned_data['username'],
            email=self.cleaned_data.get('email') or '',
            first_name=self.cleaned_data.get('first_name') or '',
            last_name=self.cleaned_data.get('last_name') or '',
            role=self.cleaned_data['role'],
        )
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            # Apply Reader subscriptions
            if user.role == User.Roles.READER:
                pubs = self.cleaned_data.get('subscriptions_to_publishers')
                journos = self.cleaned_data.get('subscriptions_to_journalists')
                if pubs:
                    user.subscriptions_to_publishers.set(pubs)
                if journos:
                    user.subscriptions_to_journalists.set(journos)
        return user

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully')
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

# Create your views here.
