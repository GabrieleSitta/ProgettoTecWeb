from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Fornitore

# Segnale che crea automaticamente un profilo fornitore quando un utente con ruolo "fornitore" viene registrato o aggiornato

User = get_user_model()

@receiver(post_save, sender=User)
def create_or_update_fornitore_profile(sender, instance, created, **kwargs):
    if created:
        # Se l'utente è appena stato creato e ha `is_fornitore=True`
        if instance.is_fornitore:
            Fornitore.objects.create(user=instance)
            print(f"Profilo Fornitore creato per {instance.username}")
    else:
        # Se l'utente è stato aggiornato e `is_fornitore` è stato impostato su True
        if instance.is_fornitore and not hasattr(instance, 'fornitore'):
            Fornitore.objects.create(user=instance)
            print(f"Profilo Fornitore creato dopo aggiornamento per {instance.username}")
