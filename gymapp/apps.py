from django.apps import AppConfig

# Definisce la configurazione dell'app "gymapp", impostando il tipo di chiave primaria predefinita 
# e si assicura che i segnali definiti nel modulo signals vengano caricati quando l'app è pronta

class GymappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gymapp'
    
    def ready(self):
        import gymapp.signals  # Importa il modulo signals