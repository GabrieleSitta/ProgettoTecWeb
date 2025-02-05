from django.db.models import Count
from gymapp.models import Product, CartOrderItem

# Funzione per generare raccomandazioni di prodotti basate sugli acquisti dell'utente 
# autenticato o sulla popolarità dei prodotti per gli utenti non autenticati
def get_recommendations(user):
    if user.is_authenticated:
        # Ottieni i prodotti acquistati dall'utente
        purchased_items = CartOrderItem.objects.filter(order__user=user)

        # Raccomanda prodotti della stessa categoria esclusi quelli acquistati
        recommended_products = Product.objects.filter(
            categoria__in=purchased_items.values_list('item__categoria', flat=True)
        ).exclude(
            id__in=purchased_items.values_list('item__id', flat=True)
        ).annotate(
            relevance=Count('id')
        ).order_by('-relevance')[:5]  # Limita a 5 prodotti

        return recommended_products

    else:
        # Raccomanda i prodotti più popolari per utenti non autenticati
        return Product.objects.annotate(
            popularity=Count('reviews')
        ).order_by('-popularity')[:5]