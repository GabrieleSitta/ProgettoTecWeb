from django.test import TestCase
from gymapp.models import Product, Category, Fornitore
from django.contrib.auth import get_user_model


# Test per verificare la corretta creazione di un prodotto, 
# assicurandosi che tutti i campi richiesti siano valorizzati correttamente

class ProductCreationTest(TestCase):
    def setUp(self):
        """
        Imposta il contesto per il test:
        - Crea un utente fornitore.
        - Crea una categoria di prodotto.
        - Crea un fornitore associato all'utente.
        """
        # Creazione di un utente di tipo fornitore
        self.user = get_user_model().objects.create_user(
            email="fornitore@example.com",  # Email del fornitore
            username="fornitore",          # Username del fornitore
            password="password123",        # Password del fornitore
            is_fornitore=True              # Flag per identificare il fornitore
        )

        # Creazione di una categoria di test
        self.category = Category.objects.create(
            title="Manubri",  # Nome corretto del campo
        )

        # Creazione di un fornitore di test associato all'utente
        self.vendor = Fornitore.objects.create(
            user=self.user,                 # Utente associato al fornitore
            title="Palestra Test",          # Nome del fornitore
            description="Descrizione del fornitore", # Descrizione
            contact="1234567890"            # Contatto del fornitore
        )

    def test_create_product(self):
        """
        Test per verificare che un prodotto venga creato correttamente
        con tutti i campi richiesti.
        """
        # Creazione di un prodotto di test
        product = Product.objects.create(
            user=self.user,                   # Utente che crea il prodotto
            categoria=self.category,          # Categoria del prodotto
            vendor=self.vendor,               # Fornitore del prodotto
            title="Manubrio 10kg",            # Titolo del prodotto
            image="manubrio.jpg",             # Immagine del prodotto
            description="Manubrio di test da 10kg", # Descrizione del prodotto
            price=25.99,                      # Prezzo del prodotto
            specifications="Specifiche di test",  # Specifiche tecniche
            stock_count="20",                 # Quantità in magazzino
            product_status="available",       # Stato del prodotto
            in_stock=True,                    # Disponibilità
            featured=False,                   # Prodotto in evidenza (False)
            digital=False,                    # Prodotto non digitale (False)
            categ_type="manubrio"             # Tipo di categoria
        )

        # Verifica che il prodotto sia stato creato correttamente
        self.assertEqual(Product.objects.count(), 1)  # Controlla che ci sia un solo prodotto nel database
        self.assertEqual(product.title, "Manubrio 10kg")  # Verifica il titolo
        self.assertEqual(product.price, 25.99)            # Verifica il prezzo
        self.assertEqual(product.stock_count, "20")       # Verifica la quantità in magazzino
        self.assertTrue(product.in_stock)                # Verifica che il prodotto sia disponibile
        self.assertEqual(product.categ_type, "manubrio") # Verifica il tipo di categoria

