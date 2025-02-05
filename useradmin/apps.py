from django.apps import AppConfig

# Configura l'applicazione Django "useradmin", specificando il tipo di chiave primaria predefinita
class UseradminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'useradmin'
