from django.contrib import admin
from userauths.models import User, Profile

# Configurazione personalizzata per la gestione degli utenti nell'admin di Django, 
# mostrando nome utente, email e biografia nella lista degli utenti
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'bio']



admin.site.register(User, UserAdmin)
admin.site.register(Profile)