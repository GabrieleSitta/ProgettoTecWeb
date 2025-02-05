from django.test import TestCase
from django.contrib.auth import get_user_model
from gymapp.models import Product, ProductReview, CartOrderItem, CartOrder
from django.urls import reverse

# Test per verificare la rimozione di un prodotto dal carrello, simulando l'interazione di un utente
class CartRemoveProductTest(TestCase):
    def setUp(self):
        # Crea un utente di prova
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com",  # Email dell'utente di prova
            username="testuser",           # Username dell'utente di prova
            password="testpassword"        # Password dell'utente di prova
        )
        # Autentica l'utente appena creato
        self.client.login(email="testuser@example.com", password="testpassword")

        # Crea un prodotto di prova con un titolo e un prezzo specificati
        self.product = Product.objects.create(title="Test Product", price=10.99)

        # Crea un ordine associato all'utente di prova
        self.order = CartOrder.objects.create(user=self.user)

        # Crea un elemento del carrello associato al prodotto e all'ordine
        self.cart_item = CartOrderItem.objects.create(
            product=self.product,   # Prodotto associato all'elemento del carrello
            qty=1,                  # Quantità del prodotto
            total=10.99,            # Totale calcolato per il prodotto
            order=self.order        # Ordine a cui appartiene l'elemento del carrello
        )

        # Definisce l'URL per rimuovere l'elemento dal carrello, utilizzando il primary key dell'elemento
        self.remove_url = reverse('gymapp:remove_from_cart', args=[self.cart_item.pk])

    def test_remove_product_from_cart(self):
        # Effettua una richiesta POST per rimuovere l'elemento dal carrello
        response = self.client.post(self.remove_url)

        # Controlla che l'elemento del carrello sia stato eliminato dal database
        self.assertFalse(CartOrderItem.objects.filter(pk=self.cart_item.pk).exists())

        # Verifica che la risposta sia un reindirizzamento (codice HTTP 302)
        self.assertEqual(response.status_code, 302)

# Test per verificare che un utente non autenticato venga reindirizzato 
# alla pagina di login quando tenta di aggiungere un prodotto al carrello
class CartUnauthenticatedTest(TestCase):
    def setUp(self):
        """
        Configura il contesto del test creando un prodotto di esempio.
        """
        self.product = Product.objects.create(
            title="Manubrio da palestra",
            price=29.99,
            stock_count=10
        )
        self.add_to_cart_url = reverse('gymapp:add_to_cart', args=[self.product.pk])

    def test_add_to_cart_redirects_if_not_authenticated(self):
        """
        Testa che un utente non autenticato venga reindirizzato alla pagina home
        quando tenta di aggiungere un prodotto al carrello.
        """
        response = self.client.post(self.add_to_cart_url, {
        'quantity': 1
        })
        # Controlla che l'utente sia reindirizzato alla pagina di login
        login_url = reverse('userauths:sign-in')  # Modifica questo in base al tuo URL di login
        self.assertRedirects(response, f"{login_url}?next={self.add_to_cart_url}")


# Test per verificare il funzionamento del modello ProductReview, 
# inclusa la creazione di recensioni, il metodo __str__ e il recupero della valutazione
class ProductReviewModelTest(TestCase):

    def setUp(self):
        # Metodo di configurazione eseguito prima di ogni test
        # Crea un utente di test utilizzando il modello utente personalizzato
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com",  # Email dell'utente di test
            username="testuser",          # Username dell'utente di test
            password="testpassword"       # Password dell'utente di test
        )
        
        # Crea un prodotto di test per associarlo alle recensioni
        self.product = Product.objects.create(
            title="Test Product",                  # Titolo del prodotto di test
            description="A test product description",  # Descrizione del prodotto
            price=100.00,                          # Prezzo del prodotto
        )
    
    def test_create_product_review(self):
        # Test per la creazione di una recensione associata a un utente e un prodotto
        review = ProductReview.objects.create(
            user=self.user,                # Utente che ha scritto la recensione
            product=self.product,          # Prodotto recensito
            review="Ottimo prodotto!",     # Testo della recensione
            rating=5                       # Valutazione assegnata (1-5)
        )
        
        # Asserzioni per verificare che la recensione sia stata creata correttamente
        self.assertEqual(ProductReview.objects.count(), 1)  # Verifica che esista una sola recensione
        self.assertEqual(review.review, "Ottimo prodotto!")  # Verifica il testo della recensione
        self.assertEqual(review.rating, 5)                  # Verifica la valutazione assegnata
        self.assertEqual(review.user, self.user)            # Verifica l'utente associato alla recensione
        self.assertEqual(review.product, self.product)      # Verifica il prodotto associato alla recensione
    
    def test_str_method(self):
        # Test per verificare il metodo __str__ del modello ProductReview
        review = ProductReview.objects.create(
            user=self.user,                # Utente che ha scritto la recensione
            product=self.product,          # Prodotto recensito
            review="Ottimo prodotto!",     # Testo della recensione
            rating=5                       # Valutazione assegnata
        )
        
        # Verifica che il metodo __str__ restituisca il titolo del prodotto
        self.assertEqual(str(review), "Test Product")
    
    def test_review_without_product(self):
        # Test per verificare la gestione di una recensione senza un prodotto associato
        review = ProductReview.objects.create(
            user=self.user,                          # Utente che ha scritto la recensione
            product=None,                            # Nessun prodotto associato
            review="Recensione senza prodotto",      # Testo della recensione
            rating=3                                 # Valutazione assegnata
        )
        
        # Verifica che il metodo __str__ restituisca un messaggio predefinito
        self.assertEqual(str(review), "Recensione senza prodotto associato")
    
    def test_get_rating_method(self):
        # Test per verificare il metodo personalizzato get_rating del modello ProductReview
        review = ProductReview.objects.create(
            user=self.user,                # Utente che ha scritto la recensione
            product=self.product,          # Prodotto recensito
            review="Ottimo prodotto!",     # Testo della recensione
            rating=5                       # Valutazione assegnata
        )
        
        # Verifica che il metodo get_rating restituisca correttamente la valutazione
        self.assertEqual(review.get_rating(), 5)