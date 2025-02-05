from django.test import TestCase
from django.contrib.auth import get_user_model
from userauths.models import User, Profile
from django.urls import reverse

# Test per verificare la funzionalità di login degli utenti, testando sia credenziali corrette che errate
class LoginViewTest(TestCase):
    def setUp(self):
        """
        Configura il contesto per il test creando un utente di prova.
        """
        # Crea un utente con credenziali valide
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com",  # Email dell'utente
            username="testuser",          # Nome utente
            password="testpassword",      # Password dell'utente
            bio="Test bio"                # Bio dell'utente
        )
        # Ottiene l'URL della view di login utilizzando il nome della route
        self.login_url = reverse('userauths:sign-in')

    def test_login_with_invalid_credentials(self):
        """
        Testa il login con credenziali errate.
        """
        # Esegue una richiesta POST alla view di login con email e password errate
        response = self.client.post(self.login_url, {
            'email': 'wrongemail@example.com',  # Email non registrata
            'password': 'wrongpassword'         # Password sbagliata
        })
        self.assertEqual(response.status_code, 302)  # Controlla che venga restituito un reindirizzamento
        self.assertRedirects(response, reverse('gymapp:base'))  # Controlla che reindirizzi alla home
        # Estrae i messaggi di risposta generati
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)  # Controlla che ci sia un solo messaggio
        # Verifica che il messaggio contenga l'avviso per credenziali errate
        self.assertIn("L'utente wrongemail@example.com non esiste.", str(messages[0]))

    def test_login_with_correct_credentials(self):
        """
        Testa il login con credenziali corrette.
        """
        # Esegue una richiesta POST alla view di login con email e password corrette
        response = self.client.post(self.login_url, {
            'email': 'testuser@example.com',  # Email valida
            'password': 'testpassword'       # Password valida
        })
        self.assertEqual(response.status_code, 302)  # Controlla che venga restituito un reindirizzamento
        self.assertRedirects(response, reverse('gymapp:base'))  # Controlla che reindirizzi alla home
        # Estrae i messaggi di risposta generati
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)  # Controlla che ci sia un solo messaggio
        # Verifica che il messaggio confermi l'accesso riuscito
        self.assertIn("Hai fatto l'accesso correttamente.", str(messages[0]))
        # Controlla che l'utente sia autenticato
        self.assertTrue(response.wsgi_request.user.is_authenticated)

# Test per verificare il corretto funzionamento del modello utente personalizzato, 
# inclusa la creazione di utenti normali e superuser
class CustomUserModelTest(TestCase):
    """
    Classe di test per verificare il comportamento del modello utente personalizzato.
    """

    def test_user_creation(self):
        """
        Test per verificare che un utente venga creato correttamente utilizzando il modello personalizzato.
        """
        # Creazione di un utente con dati specifici
        user = User.objects.create_user(
            email="testuser@example.com",  # Email dell'utente
            username="testuser",           # Nome utente
            password="testpassword",       # Password
            bio="Test bio content"         # Contenuto del campo biografico
        )

        # Verifica che esista un solo utente nel database
        self.assertEqual(User.objects.count(), 1)

        # Controlla che i campi dell'utente corrispondano ai valori forniti
        self.assertEqual(user.email, "testuser@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.bio, "Test bio content")

        # Verifica che la password sia stata impostata correttamente
        self.assertTrue(user.check_password("testpassword"))

    def test_superuser_creation(self):
        """
        Test per verificare che un superuser venga creato correttamente.
        """
        # Creazione di un superuser con dati specifici
        superuser = User.objects.create_superuser(
            email="adminuser@example.com",  # Email del superuser
            username="adminuser",           # Nome utente del superuser
            password="adminpassword"        # Password del superuser
        )

        # Verifica che esista un solo utente (il superuser) nel database
        self.assertEqual(User.objects.count(), 1)

        # Controlla che il superuser abbia i permessi di amministrazione
        self.assertTrue(superuser.is_superuser)  # Verifica che sia un superuser
        self.assertTrue(superuser.is_staff)     # Verifica che sia staff

        # Controlla che i campi del superuser corrispondano ai valori forniti
        self.assertEqual(superuser.email, "adminuser@example.com")
        self.assertEqual(superuser.username, "adminuser")

# Test per verificare il corretto funzionamento del modello Profile,inclusa la creazione automatica, l'eliminazione 
# associata all'utente e i valori predefiniti dei campi
class ProfileModelTest(TestCase):
    def setUp(self):
        """
        Imposta il contesto per i test creando un utente e verificando la
        creazione automatica di un profilo associato.
        """
        # Creazione di un utente di test
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com",  # Email dell'utente di test
            username="testuser",           # Username dell'utente di test
            password="testpassword"        # Password dell'utente di test
        )

    def test_profile_creation(self):
        """
        Test per verificare che la creazione di un utente generi automaticamente un profilo associato.
        """
        # Recupera il profilo associato all'utente di test
        profile = Profile.objects.get(user=self.user)

        # Verifica che il profilo esista
        self.assertIsNotNone(profile)

        # Verifica che il profilo sia correttamente associato all'utente
        self.assertEqual(profile.user, self.user)

    def test_profile_deletion_with_user(self):
        """
        Test per verificare che l'eliminazione di un utente comporti l'eliminazione
        automatica del profilo associato.
        """
        # Recupera il profilo associato all'utente
        profile = Profile.objects.get(user=self.user)

        # Salva la primary key del profilo per controlli futuri
        profile_pk = profile.pk

        # Elimina l'utente
        self.user.delete()

        # Verifica che il profilo associato non esista più
        with self.assertRaises(Profile.DoesNotExist):
            Profile.objects.get(pk=profile_pk)

    def test_profile_fields_default_values(self):
        """
        Test per verificare che i campi del profilo abbiano valori di default corretti.
        """
        # Recupera il profilo associato all'utente di test
        profile = Profile.objects.get(user=self.user)

        # Controlla che l'immagine non sia impostata (vuota)
        self.assertFalse(bool(profile.image))

        # Controlla che il campo `full_name` sia None
        self.assertEqual(profile.full_name, None)

        # Controlla che il campo `bio` sia una stringa vuota
        self.assertEqual(profile.bio, "")

        # Controlla che il campo `phone` sia una stringa vuota
        self.assertEqual(profile.phone, "")

    def test_profile_str_method(self):
        """
        Test per verificare che il metodo __str__ restituisca il valore atteso.
        """
        # Recupera il profilo associato all'utente di test
        profile = Profile.objects.get(user=self.user)

        # Imposta valori di test per `full_name` e `bio`
        profile.full_name = "John Doe"
        profile.bio = "Bio di test"
        profile.save()

        # Verifica che il metodo __str__ restituisca la stringa formattata correttamente
        expected_str = f"{self.user.username} - {profile.full_name} - {profile.bio}"
        self.assertEqual(str(profile), expected_str)