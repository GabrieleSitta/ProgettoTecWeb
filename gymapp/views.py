from django.shortcuts import render, redirect, get_object_or_404
from gymapp.models import Product, Fornitore, CartOrder, CartOrderItem, ProductReview, FornitoreReview
from gymapp.forms import ProductReviewForm, FornitoreReviewForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
import random
from django.db.models import Count
from gymapp.utils import get_recommendations
from decimal import Decimal
from django.utils.timezone import now
import random

#Home
def base(request):
    """
    Vista per la homepage che include le raccomandazioni.
    """
    # Ottenere raccomandazioni
    recommended_products = get_recommendations(request.user)

    # Dati per la pagina
    context = {
        "recommended_products": recommended_products,
    }    
    return render(request, 'partials/base.html',context)


#Prodotti
def product_detail_view(request, pid):
    prodotto = Product.objects.get(pid=pid)
    product = get_object_or_404 (Product, pid=pid)#prende l'id del prodotto che sto visualizzando
    products = Product.objects.filter(categoria=prodotto.categoria).exclude(pid=product.pid)#Mostra i prodotti correlati senza quello che sto visualizzando
    
    #Visualizzare tutte le review
    reviews = ProductReview.objects.filter(product = prodotto).order_by("-date")

    #inizializzo il form
    form = ProductReviewForm()

    #Aggiunta al carrello

    if request.method == "POST" and "add_to_cart" in request.POST:
        qty = int(request.POST.get("quantity", 1))

        if request.user.is_authenticated:
            cart, created = CartOrder.objects.get_or_create(user=request.user, paid_status=False)
            cart_item, created = CartOrderItem.objects.get_or_create(order=cart, item=prodotto)
            cart_item.qty += qty
            cart_item.save()

            messages.success(request, "Prodotto aggiunto al carrello!")
        else:
            messages.error(request, "Devi effettuare il login per aggiungere prodotti al carrello.")

        return redirect("gymapp:dettagli_prodotto", pid=pid)

    #Product Review form
    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = prodotto
            review.user = request.user  # Assicurati che l'utente sia autenticato
            review.save()
            return redirect('gymapp:dettagli_prodotto', pid=pid)  # Ricarica la pagina prodotto
    else:
        form = ProductReviewForm()

    context = {
        "p" : prodotto,
        "reviews" : reviews,
        "review_form" : form,
        "products": products,
    }

    return render (request, "partials/dettagli_prodotto.html", context)

def manubri(request):
    manubri = Product.objects.filter(categ_type="manubrio")

    context = {
        "manubri": manubri
    }

    return render(request, 'core/pesistica/manubri.html', context)

def panche(request):
    bench = Product.objects.filter(categ_type="panca")

    context = {
        "bench": bench,
    }

    return render(request, 'core/pesistica/panche.html', context)

def bilancieri(request):
    barbell = Product.objects.filter(categ_type="bilanciere")

    context = {
        "barbell": barbell,
    }

    return render(request, 'core/pesistica/bilancieri.html',context)

def dischi(request):
    pesi = Product.objects.filter(categ_type="disco")

    context = {
        "pesi": pesi,
    }

    return render(request, 'core/pesistica/dischi.html', context)

def collari(request):
    ring = Product.objects.filter(categ_type="collare")

    context = {
        "ring": ring,
    }

    return render(request, 'core/pesistica/collari.html',context)

def tapis(request):
    tapisrulant = Product.objects.filter(categ_type="tapisrulant")

    context = {
        "tapisrulant": tapisrulant,
    }
    return render(request, 'core/cardio/tapis.html',context)

def vogatori(request):
    vogatori = Product.objects.filter(categ_type="vogatore")

    context = {
        "vogatori": vogatori,
    }

    return render(request, 'core/cardio/vogatori.html',context)

def bike(request):
    bike = Product.objects.filter(categ_type="bike")

    context = {
        "bike": bike,
    }
    return render(request, 'core/cardio/bici.html',context)

def unica(request):
    unica = Product.objects.filter(categ_type="unica")

    context = {
        "unica": unica,
    }
    return render(request, 'core/multigym/unica.html',context)

def rack(request):
    rack = Product.objects.filter(categ_type="rack")

    context = {
        "rack": rack,
    }
    return render(request, 'core/multigym/rack.html',context)

def addome(request):
    addome = Product.objects.filter(categ_type="addome")

    context = {
        "addome": addome,
    }
    return render(request, 'core/multigym/addome.html',context)

def lombare(request):
    lombare = Product.objects.filter(categ_type="lombare")

    context = {
        "lombare": lombare,
    }
    return render(request, 'core/multigym/lombare.html',context)



#Contattaci
def contatti(request):
    return render(request, 'partials/contatti.html')  # Specifica il template per la pagina Contattaci


#Privacy
def privacy(request):
    return render(request, 'partials/privacy.html') 


#Ricerca
def search(request):
    query = request.GET.get("q")  # Ottieni la query dalla barra di ricerca
    
    if not query:
        context = {
            "products": [],
            "query": query,
            "error": "Inserisci un termine di ricerca valido.",
        }
        return render(request, 'partials/ricerca.html', context)


    products = Product.objects.filter(
        title__icontains=query
    )

    # Aggiungi ricerca per descrizione
    products = products | Product.objects.filter(description__icontains=query)

    # Controlla se la query è un numero e aggiungi ricerca per prezzo
    if query.isdigit():
        products = products | Product.objects.filter(price=query)

    # Ordina i risultati per data (decrescente)
    products = products.order_by("-date")

    context = {
        "products": products.distinct(),  # Evita duplicati
        "query": query,
    }
    context = {
        "products": products,
        "query": query,
    }

    return render (request, 'partials/ricerca.html', context)


#Fornitore
def fornitore_list(request, vid):
    vendor = Fornitore.objects.get(vid=vid)
    prodotti = Product.objects.filter(vendor= vendor)

    reviews = FornitoreReview.objects.filter(fornitore=vendor).order_by('-date')

    # Inizializza il modulo per le recensioni
    form = FornitoreReviewForm()

    # Gestione POST per invio recensioni
    if request.method == 'POST':
        form = FornitoreReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.fornitore = vendor
            review.user = request.user
            review.save()
            messages.success(request, "Recensione inviata con successo!")
            return redirect('gymapp:fornitore_list', vid=vid)
    context ={
        "vendor" : vendor,
        "prodotti" : prodotti,
        "reviews": reviews,
        "form": form,

    }

    return render (request, "partials/fornitore.html", context)


#Carrello
@login_required
def cart_view(request):
    # Recupera il carrello dell'utente loggato
    cart, _ = CartOrder.objects.get_or_create(
        user=request.user,
        product_status="processing"
    )
    # Recupera gli elementi associati a questo carrello
    cart_items = CartOrderItem.objects.filter(order=cart)
    
    # Calcola il totale del carrello
    total = sum(item.total for item in cart_items)
    
    context = {
        "cart": cart,
        "cart_items": cart_items,
        "total": total,
    }
    return render(request, "partials/cart.html", context)

@login_required
def add_to_cart(request, pid):
    product = get_object_or_404(Product, id=pid)  # Prendi il prodotto
    cart, created = CartOrder.objects.get_or_create(user=request.user, product_status="processing")
    
    if not request.user.is_authenticated:
        messages.error(request, "Devi effettuare il login per aggiungere prodotti al carrello.")
        return render(request,"partials/dettagli_prodotto.html")  # Reindirizza alla pagina di login
    
    
    cart, created = CartOrder.objects.get_or_create(user=request.user, product_status="processing")
    
    # Cerca se l'elemento è già nel carrello
    cart_item, created = CartOrderItem.objects.get_or_create(
        order=cart,
        product=product,  # Associa il prodotto
    )
    
    if not created:
        # Se il prodotto è già nel carrello, aumenta la quantità
        cart_item.qty += 1
        cart_item.total = cart_item.qty * product.price
    else:
        # Se è un nuovo elemento, imposta il prezzo e il totale
        cart_item.qty = 1
        cart_item.price = product.price
        cart_item.total = product.price

    cart_item.save()
    messages.success(request, "Prodotto aggiunto al carrello!")
    return redirect('gymapp:cart')

@login_required
def update_cart_item(request, pk):
    if request.method == 'POST':
        item = get_object_or_404(CartOrderItem, pk=pk)
        new_quantity = int(request.POST.get('quantity', 1))
        if new_quantity > 0:
            item.qty = new_quantity
            item.total = item.price * new_quantity
            item.save()
        else:
            # Se la quantità è 0, rimuovi l'elemento dal carrello
            item.delete()
    return redirect('gymapp:cart')

@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartOrderItem, pk=pk)
    cart_item.delete()
    return redirect('gymapp:cart')  # Torna alla pagina del carrello


#Pagamento
@login_required
def checkout_view(request):
    # Verifica se il carrello è vuoto
    cart_items = CartOrderItem.objects.filter(order__user=request.user, order__product_status="processing")
    if not cart_items.exists():
        messages.error(request, "Il tuo carrello è vuoto. Aggiungi dei prodotti prima di procedere al checkout.")
        return redirect('gymapp:cart')  # Reindirizza alla pagina del carrello

    if request.method == 'POST':
        # Recupera i dati del modulo
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        address_line2 = request.POST.get('address_line2')
        city = request.POST.get('city')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        additional_info = request.POST.get('additional_info')
        payment_method = request.POST.get('payment_method')

        # Verifica se tutti i campi obbligatori sono completi
        if not (first_name and last_name and address and city and postcode and phone and email and payment_method):
            messages.error(request, "Per favore compila tutti i campi obbligatori.")
            return redirect('gymapp:checkout')

        # Generazione di un IBAN casuale
        country_code = "IT"  # Codice del paese per l'Italia
        check_digits = f"{random.randint(10, 99)}"  # Due cifre di controllo
        bank_code = "".join([str(random.randint(0, 9)) for _ in range(5)])  # Codice banca (5 cifre)
        branch_code = "".join([str(random.randint(0, 9)) for _ in range(5)])  # Codice filiale (5 cifre)
        account_number = "".join([str(random.randint(0, 9)) for _ in range(12)])  # Numero conto (12 cifre)
        iban = f"{country_code}{check_digits}{bank_code}{branch_code}{account_number}"


        # Logica per il pagamento alla consegna
        if payment_method == 'cod':
            # Invia l'email di conferma
            subject = "Conferma Ordine - GymShop"
            message = f"""
            Grazie per il tuo ordine, {first_name} {last_name}!

            Dettagli ordine:
            - Indirizzo: {address}, {address_line2 or ''}
            - Città: {city}, CAP: {postcode}
            - Telefono: {phone}
            - Email: {email}
            - Pagamento: Bonifico SEPA
            - IBAN: {iban}
            - Il prodotto sarà spedito immediatamente dopo l'accredito sul conto corrente. La consegna si considera completata al momento della firma di ricezione al corriere.

            Prodotti ordinati:
            """
            cart_items = CartOrderItem.objects.filter(order__user=request.user, order__product_status="processing")
            for item in cart_items:
                message += f"- {item.product.title} × {item.qty}: €{item.total}\n"
                
            message += f"\nTotale ordine: €{sum(item.total for item in cart_items):.2f}\n\n"
            message += "Il tuo ordine verrà elaborato e spedito a breve.\n\nGrazie per aver acquistato da noi!"

            # Invia email
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                )

                messages.success(request, "Pagamento completato con successo! Email inviata.")
                return redirect('gymapp:payment_completed')  # Redirect alla pagina di successo
            except Exception as e:
                messages.error(request, f"Errore nell'invio dell'email: {str(e)}")
                return redirect('gymapp:payment_failed')  # Redirect alla pagina di fallimento
            
        else:
            # Se non è pagamento alla consegna, fallo fallire
            messages.error(request, "Metodo di pagamento non supportato.")
            return redirect('gymapp:payment_failed')
        

    # Visualizza la pagina di checkout
    cart_items = CartOrderItem.objects.filter(order__user=request.user, order__product_status="processing")
    total = sum(item.total for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, "partials/checkout.html", context)

def payment_completed_view(request):
     # Recupera il carrello e i dati per il rendering della pagina di checkout
    cart = get_object_or_404(CartOrder, user=request.user, product_status="processing")
    cart_items = CartOrderItem.objects.filter(order=cart)
    shipping_fee = Decimal("10.00")
    total = sum(item.total for item in cart_items)
    grand_total = total + shipping_fee

    # Ottieni la data odierna
    current_date = now().strftime("%d/%m/%Y")

    # Genera un codice randomico per l'ordine
    order_code = f"ORD-{random.randint(1000, 9999)}"
    
    context = {
        "cart_items": cart_items,
        "total": total,
        "shipping_fee": shipping_fee,
        "grand_total": grand_total,
        "date": current_date,
        "order_code": order_code,
    }
    cart.product_status = "archived"    
    cart.save()
    return render (request, 'partials/payment-completed.html', context)

def payment_failed_view(request):
    return render (request, 'partials/payment-failed.html')


#Reccomandation System
def get_recommendations(user):
    """
    Raccomanda prodotti basati sulla categoria degli articoli già acquistati dall'utente.
    """
    if not user.is_authenticated:
        return Product.objects.filter(status=True, featured=True)[:5]  # Prodotti in evidenza per utenti non autenticati

    # Recupera tutte le categorie dei prodotti acquistati dall'utente
    purchased_items = CartOrderItem.objects.filter(
        order__user=user,
        order__product_status="archived"  # Solo ordini completati
    ).values_list('product__categoria', flat=True).distinct()

    # Raccomanda prodotti dalla stessa categoria degli articoli acquistati
    recommended_products = Product.objects.filter(
        categoria__in=purchased_items,  # Prodotti con la stessa categoria
        status=True,  # Solo prodotti attivi
        in_stock=True  # Solo prodotti in stock
    ).exclude(
        cartorderitem__order__user=user  # Escludi prodotti già acquistati dall'utente
    ).annotate(
        relevance=Count('id')
    ).order_by('-relevance')[:5]  # Limita a 5 prodotti

    return recommended_products

