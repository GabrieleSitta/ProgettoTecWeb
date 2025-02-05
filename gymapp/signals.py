from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from gymapp.models import Product
from django.contrib.auth import get_user_model

# Segnale che invia un'email a tutti gli utenti registrati quando un nuovo prodotto viene aggiunto al catalogo


@receiver(post_save, sender=Product)
def send_product_update_email(sender, instance, created, **kwargs):
    """
    Invia un'email agli utenti quando viene aggiunto un nuovo prodotto.
    """
    if created:  # Verifica se il prodotto è stato appena creato
        # Ottieni tutti gli utenti registrati
        User = get_user_model()
        user_emails = User.objects.values_list('email', flat=True)

        # Componi l'email
        subject = "Nuovo prodotto disponibile nel catalogo!"
        message = f"Un nuovo prodotto è stato aggiunto al nostro catalogo: {instance.title}.\n" \
                  f"Prezzo: €{instance.price}\n" \
                  f"Descrizione: {instance.description}\n\n" \
                  f"Visita il nostro sito per maggiori dettagli!"
        from_email = "hostgymapp@gmail.com"

        # Invia l'email a tutti gli utenti
        send_mail(subject, message, from_email, user_emails)
