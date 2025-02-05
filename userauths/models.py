from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

# Modello personalizzato per la gestione degli utenti, estendendo il modello predefinito di Django
# e aggiungendo campi extra come email univoca, biografia e flag per i fornitori
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    bio = models.CharField(max_length=100)
    is_fornitore = models.BooleanField(default=False)  # Campo per distinguere i fornitori

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    


#Modifica del Profilo Utente
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #Quando elimino un utente elimino anche il suo profilo
    image = models.ImageField(upload_to="image")
    full_name = models.CharField(max_length=200, null=True, blank=True)
    bio= models.CharField(max_length=200)
    phone = models.CharField(max_length=200) #+39 3491284782

    def __str__(self):
        return f"{self.user.username} - {self.full_name} - {self.bio}"



#Permette ad ogni utente che si registra di avere la sua pagina di profilo
def create_user_profile (sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)