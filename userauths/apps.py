from django.apps import AppConfig

# Configurazione dell'applicazione "userauths" in Django, 
# specificando il tipo di chiave primaria predefinita per i modelli
class UserauthsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userauths'
