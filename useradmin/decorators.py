from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

# Limita l'accesso alle viste solo agli amministratori (superuser)
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser != True:
            messages.warning(request, "Non sei autorizzato ad accedere a questa pagina")
            return redirect('gymapp:base')
        
        return view_func(request, *args, **kwargs)

    return wrapper

# Limita l'accesso alle viste solo agli utenti con ruolo di fornitore
def fornitore_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_fornitore:
            return HttpResponseForbidden("Non sei autorizzato ad accedere a questa pagina.")
        return view_func(request, *args, **kwargs)
    return wrapper