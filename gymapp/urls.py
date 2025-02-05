from django.urls import path
from gymapp import views


app_name = "gymapp"

urlpatterns = [
    #Homepage
    path("", views.base, name='base'),

    #Prodotti
    path('manubri/', views.manubri, name='manubri'),
    path('bilancieri/', views.bilancieri, name='bilancieri'),
    path('dischi/', views.dischi, name='dischi'),
    path('collari/', views.collari, name='collari'),
    path('tapisrulant/', views.tapis, name='tapis'),
    path('vogatori/', views.vogatori, name='vogatori'),
    path('cyclette/', views.bike, name='cyclette'),
    path('unica/', views.unica, name='unica'),
    path('rack/', views.rack, name='rack' ),
    path('addome/', views.addome, name='addome'),
    path('lombare/', views.lombare, name='lombare'),
    path('panche/', views.panche, name='panche'),
    path('dettagli_prodotto/<pid>/', views.product_detail_view, name ='dettagli_prodotto'),

    #Menù
    path('contatti/', views.contatti, name='contatti'),  
    path('search/', views.search, name='search'),

    #Privacy
    path('privacy/', views.privacy, name='privacy'),

    #Fornitore
    path('fornitore/<vid>/', views.fornitore_list, name ='fornitore_list'),

    #Aggiungi Recensione
    path('product/<int:pid>/', views.product_detail_view, name='product_details'),

    #Carrello
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:pid>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:pk>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),

    #Checkout
    path('checkout/', views.checkout_view, name='checkout'),

    #Pagamento
    path('payment_completed/', views.payment_completed_view, name='payment_completed'),
    path('payment_failed/', views.payment_failed_view, name='payment_failed'),


]


