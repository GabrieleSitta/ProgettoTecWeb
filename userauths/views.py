from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm, ProfileForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
#from django.conf import settings
from .models import User, Profile
from django.contrib.auth.decorators import login_required
#User = settings.AUTH_USER_MODEL


# Registrazione.
def register_view(request):

    if request.method =="POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, il tuo account è stato creato correttamente.")
            new_user = authenticate(username = form.cleaned_data['email'],
                                    password = form.cleaned_data['password1']                        
            )
            login(request, new_user)
            return redirect("gymapp:base")


    else:
        print("L'utente non può essere registrato")
        form = UserRegisterForm()
    

    context = {
        'form': form,
    }
    return render(request, "userauths/sign-up.html", context)

#Login.
def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hai già fatto l'accesso")
        return redirect("gymapp:base")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Hai fatto l'accesso correttamente.")
                return redirect("gymapp:base")
            else:
                messages.warning(request, f"L'utente non esiste, crea un account. ")
                return redirect("gymapp:base")

        except:
            messages.warning(request, f"L'utente {email} non esiste.")
            return redirect("gymapp:base")


    return render(request, "userauths/sign-in.html")

#logout
def logout_view(request):
    logout(request)
    messages.success(request, f"Ti sei disconnesso")
    return redirect("gymapp:base")


@login_required
def user_view(request):
    user = request.user
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        # Aggiornamento delle informazioni utente
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        # Validazione e salvataggio
        if first_name and last_name and email:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            messages.success(request, "Il tuo profilo è stato aggiornato con successo.")
        else:
            messages.error(request, "Tutti i campi sono obbligatori.")

    # Render della pagina del profilo
    context = {
        'profile':profile,
        'user': user,
    }
    return render(request, 'userauths/user-page.html', context)


def profile_update(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile_save = form.save(commit=False)
            profile_save.user = request.user
            profile_save.save()
            messages.success(request, "Profilo aggiornato con successo")
            return redirect ("userauths:user-view")
    else:
        form = ProfileForm(instance=profile)


    context = {
        "form": form,
        "profile":profile
    }

    return render (request, "userauths/profile-edit.html",context)

