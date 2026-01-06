from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login
from django import forms
from django.contrib import messages
from publications.models import Publisher

User = get_user_model()

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=User.Roles.choices)
    subscriptions_to_publishers = forms.ModelMultipleChoiceField(
        queryset=Publisher.objects.all(),
        required=False,
        widget=forms.SelectMultiple
    )
    subscriptions_to_journalists = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role=User.Roles.JOURNALIST),
        required=False,
        widget=forms.SelectMultiple
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rec_pubs = Publisher.objects.all()[:3]
        rec_journos = User.objects.filter(role=User.Roles.JOURNALIST)[:3]
        self.fields['subscriptions_to_publishers'].initial = list(rec_pubs.values_list('id', flat=True))
        self.fields['subscriptions_to_journalists'].initial = list(rec_journos.values_list('id', flat=True))

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
