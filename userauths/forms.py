from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User, Profile

# Modulo per la registrazione di un nuovo utente, estendendo il modulo di creazione utente predefinito di Django
class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email']

# Modulo per la gestione del profilo utente, includendo campi con placeholder per facilitare la compilazione
class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Full Name"}))
    bio = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Bio"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Phone"}))

    class Meta:
        model = Profile
        fields = ['full_name', 'image', 'bio', 'phone']