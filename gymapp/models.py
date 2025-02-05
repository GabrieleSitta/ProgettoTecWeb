from django.db import models
from django.conf import settings
from shortuuid.django_fields import ShortUUIDField
from userauths.models import User
from django.utils.html import mark_safe
from unicodedata import decimal

# Definisce insiemi di opzioni predefinite per i campi dei modelli Django, 
# utilizzati per gestire lo stato degli ordini, la visibilità dei prodotti, 
# le valutazioni degli utenti e le categorie di articoli

STATUS_CHOICE = (
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)


STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)

RATING = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)

CATEGORY = (
    ("manubrio", "Manubrio"),
    ("panca", "Panca"),
    ("bike", "Bike"),
    ("bilanciere", "Bilanciere"),
    ("collare", "Collare"),
    ("disco", "Disco"),
    ("lombare", "Lombare"),
    ("rack", "Rack"),
    ("tapisrulant", "TapisRulant"),
    ("unica", "Unica"),
    ("vogatore", "Vogatore"),
    ("addome", "Addome"),
)



# Genera il percorso di salvataggio per i file caricati dagli utenti, 
# organizzandoli in cartelle con il loro ID utente
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

# Modello per le categorie dei prodotti, con un identificatore univoco personalizzato, 
# titolo, immagine e un metodo per visualizzare un'anteprima dell'immagine nell'admin di Django
class Category(models.Model):

    cid  = ShortUUIDField(unique=True, length= 10, max_length=20, prefix ="cat", alphabet = "abcdefgh12345")
    
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="category")

    # Imposta il nome plurale per il modello nell'admin di Django
    class Meta:
        verbose_name_plural = "Categories"

    # Restituisce un'anteprima dell'immagine come HTML, utile per l'admin di Django
    def category_image(self):
        return mark_safe ('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    # Rappresentazione testuale dell'oggetto, restituisce il titolo della categoria
    def __str__(self):
        return self.title


# Modello per i fornitori, con un identificatore univoco personalizzato, informazioni di contatto, 
# valutazioni e un'anteprima dell'immagine nell'admin di Django
class Fornitore(models.Model):
    vid  = ShortUUIDField(unique=True, length= 10, max_length=20, prefix ="forn", alphabet = "abcdefgh12345")
    
    title = models.CharField(max_length=200, default ="Nestify")
    image = models.ImageField(upload_to= user_directory_path)
    description = models.TextField(null= True, blank=True)

    address = models.CharField(max_length=200, default="123 Via Emilia")
    contact = models.CharField(max_length=200, default="+123 (059) 798")
    chat_resp_time = models.CharField(max_length=200, default="100")
    spedizione_in_tempo = models.CharField(max_length=200, default="100")
    valutazione_autentica = models.CharField(max_length=200, default="100")
    days_return = models.CharField(max_length=200, default="100")
    periodo_rimborso = models.CharField(max_length=200, default="100")


    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Fornitori"
    
    def fornitore_image(self):
        return mark_safe ('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title


# Modello per la gestione dei prodotti, con identificatore univoco,collegamenti a utente, 
# categoria e fornitore, dettagli sul prodotto,disponibilità, stato e informazioni di catalogazione
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length= 10, max_length=30, alphabet = "abcdefgh12345")
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    categoria = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    vendor = models.ForeignKey(Fornitore, on_delete=models.SET_NULL, null=True, related_name="vendor")
    

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to=user_directory_path)
    description = models.TextField(null= True, blank=True)
    
    price = models.DecimalField(max_digits=99999999999999, decimal_places=2, default="1.99")

    specifications= models.TextField(null=True, blank=True)
    stock_count = models.CharField(max_length=100, default="10")
    

    product_status = models.CharField(choices= STATUS, max_length=10, default="in_review")

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)


    categ_type = models.CharField(choices=CATEGORY, max_length=40, default="manubrio")


    sku = ShortUUIDField(unique=True, length= 4, max_length=10, prefix ="sku", alphabet = "1234567890")

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)


    class Meta:
        verbose_name_plural = "Prodotti"

    def product_image(self):
        return mark_safe ('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title

# Modello per la gestione delle immagini aggiuntive dei prodotti, 
# consentendo il caricamento di più immagini per un singolo prodotto
class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "Product Images"


####################################### Cart, Order, Order Items and Adress #################################################################
####################################### Cart, Order, Order Items and Adress #################################################################
####################################### Cart, Order, Order Items and Adress #################################################################
####################################### Cart, Order, Order Items and Adress #################################################################
####################################### Cart, Order, Order Items and Adress #################################################################


# Modello per la gestione degli ordini nel carrello, includendo l'utente, 
# il prezzo totale, lo stato del pagamento e la data dell'ordine
class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=99999999999999, decimal_places=2, default="1.99")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices= STATUS_CHOICE, max_length=30, default="processing")

    class Meta:
        verbose_name_plural = "Cart Order"

# Modello per la gestione degli articoli all'interno di un ordine, 
# collegando ogni prodotto all'ordine, includendo dettagli come quantità, prezzo, totale e un'anteprima dell'immagine
class CartOrderItem(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True, blank=True)  # Collega al prodotto
    invoice_no = models.CharField(max_length=200) # Numero di fattura associato all'ordine
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=99999999999999, decimal_places=2, default="1.99")
    total = models.DecimalField(max_digits=99999999999999, decimal_places=2, default="1.99")


    class Meta:
        verbose_name_plural = "Cart Items"

    def order_img(self):
        return mark_safe ('<img src="/media/%s" width="50" height="50" />' % (self.image))


####################################### Product Review, address #################################################################
####################################### Product Review, address #################################################################
####################################### Product Review, address #################################################################

# Modello per la gestione delle recensioni sui prodotti, includendo l'utente, il prodotto recensito, 
# il testo della recensione, la valutazione e la data di creazione
class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null= True)
    product =  models.ForeignKey(Product, on_delete=models.SET_NULL, null= True, related_name="reviews")
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        if self.product:
            return self.product.title
        return "Recensione senza prodotto associato"
    
    # Restituisce la valutazione della recensione
    def get_rating(self):
        return self.rating
    
# Modello per la gestione degli indirizzi degli utenti, includendo l'utente associato, 
# l'indirizzo e un indicatore di stato
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null= True)
    address = models.CharField(max_length=200, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"


# Modello per la gestione delle recensioni dei fornitori, collegando ogni recensione 
# a un fornitore e a un utente, includendo valutazione, commento e data di creazione
class FornitoreReview(models.Model):
    fornitore = models.ForeignKey(Fornitore, on_delete=models.CASCADE, related_name="reviews")  # Collegamento al fornitore
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Utente che lascia la recensione
    rating = models.IntegerField(choices=RATING, default=None)  # Valutazione (es: 1-5)
    comment = models.TextField()  # Commento della recensione
    date = models.DateTimeField(auto_now_add=True)  # Data di creazione della recensione

    class Meta:
        verbose_name_plural = "Recensioni Fornitori"

    def __str__(self):
        return f"Review for {self.fornitore.title} by {self.user.username}"