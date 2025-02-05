from django.contrib import admin
from gymapp.models import Product, Category, Fornitore, CartOrder, CartOrderItem, ProductImages, ProductReview, Address, FornitoreReview


# Permette di gestire le immagini del prodotto direttamente dalla pagina di amministrazione Django
class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

# Permette di visualizzare e modificare le immagini del prodotto direttamente nella pagina di amministrazione del prodotto
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user', 'title', 'product_image', 'price', 'featured', 'product_status', 'categ_type', 'pid']

# Definisce i campi visibili nella lista delle categorie nell'admin di Django
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']

# Definisce i campi visibili nella lista dei fornitori nell'admin di Django
class FornitoreAdmin(admin.ModelAdmin):
    list_display = ['title', 'fornitore_image']  

# Mostra i dettagli principali degli ordini nel pannello di amministrazione Django
class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'price', 'paid_status', 'order_date', 'product_status' ]

 # Mostra gli elementi di un ordine nel pannello di amministrazione, inclusi dettagli come quantità, prezzo e totale
class CartOrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product','invoice_no', 'item', 'image', 'qty', 'price', 'total']   

# Mostra le recensioni dei prodotti con l'utente, il prodotto recensito, il commento e il voto
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']

# Mostra le recensioni dei fornitori nell'admin di Django, includendo il fornitore recensito, l'utente, il commento, il punteggio e la data della recensione
class FornitoreReviewAdmin(admin.ModelAdmin):
    list_display = ['fornitore', 'user', 'comment', 'rating', 'date']

 # Mostra gli indirizzi salvati dagli utenti nell'admin di Django, inclusi l'utente associato, l'indirizzo e lo stato (attivo/inattivo)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'status']
  

#Registra i diversi modelli all'interno del pannello di amministrazione 
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Fornitore, FornitoreAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItem, CartOrderItemAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(FornitoreReview,FornitoreReviewAdmin)
admin.site.register(Address, AddressAdmin)




#admin name= gabbuz
#admin pass=12345