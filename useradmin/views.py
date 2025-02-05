from pyexpat.errors import messages
from django.contrib import messages
from django.shortcuts import render,redirect
from gymapp.models import CartOrder, Product, Category, CartOrderItem, Fornitore
from django.db.models import Sum
from userauths.models import User
from useradmin.forms import AddProductForm, FornitoreForm
from useradmin.decorators import admin_required, fornitore_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import datetime



@fornitore_required
def dashboard(request):
    revenue = CartOrder.objects.aggregate(price=Sum("price"))
    total_orders_count = CartOrder.objects.all()
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    new_costumers = User.objects.all().order_by("-id")
    latest_orders = CartOrderItem.objects.all()

    this_month = datetime.datetime.now().month

    monthly_revenue = CartOrder.objects.filter(order_date__month = this_month).aggregate(price=Sum("price"))

    fornitore = None
    if request.user.is_authenticated and hasattr(request.user, 'fornitore'):
        fornitore = request.user.fornitore

    context = {
        "revenue":revenue,
        "total_orders_count":total_orders_count,
        "all_products":all_products,
        "all_categories":all_categories,
        "new_costumers":new_costumers,
        "latest_orders":latest_orders,
        "monthly_revenue":monthly_revenue,
        'fornitore': fornitore,
    }

    return render(request, "useradmin/dashboard.html", context)

@fornitore_required
def products(request):
    all_products = Product.objects.all().order_by("-id")
    all_categories = Category.objects.all()

    context = {
        "all_products":all_products,
        "all_categories":all_categories,
      }
    
    return render(request, "useradmin/products.html", context)

@fornitore_required
def add_product(request):
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            form.save_m2m()
            return redirect("useradmin:dashboard")
    else:
        form = AddProductForm()
        
    context = {
        "form": form
    }

    return render(request, "useradmin/add-product.html", context)

@admin_required
def edit_product(request, pid):
    product = Product.objects.get(pid=pid)
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            form.save_m2m()
            return redirect("useradmin:edit_product", product.pid)
    else:
        form = AddProductForm(instance=product)
        
    context = {
        "form": form,
        "product": product
    }

    return render(request, "useradmin/edit-product.html", context)

@admin_required
def delete_product(request, pid):
    product = Product.objects.get(pid=pid)
    product.delete()
    return redirect ("useradmin:products")


#Modifica Permessi
@csrf_exempt
@admin_required
def manage_users_view(request):
    if request.method == "POST":
        # Gestione richiesta AJAX per modificare i ruoli
        user_id = request.POST.get("user_id")
        action = request.POST.get("action")
        try:
            user = User.objects.get(id=user_id)
            if action == "make_fornitore":
                user.is_fornitore = True
                user.save()
                return JsonResponse({"success": True, "message": f"{user.username} è ora un Fornitore."})
            elif action == "remove_fornitore":
                user.is_fornitore = False
                user.save()
                return JsonResponse({"success": True, "message": f"{user.username} non è più un Fornitore."})
            else:
                return JsonResponse({"success": False, "message": "Azione non valida."}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"success": False, "message": "Utente non trovato."}, status=404)
    
    # Caricamento della pagina con lista utenti
    users = User.objects.all()
    return render(request, "useradmin/manage_users.html", {"users": users})


def fornitore_view(request):
    # Recupera il fornitore associato all'utente autenticato
    user = request.user
    fornitore, created = Fornitore.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        # Aggiornamento delle informazioni utente
        title = request.POST.get('title')
        description = request.POST.get('description')
        email = request.POST.get('email')

        # Validazione e salvataggio
        if title and email:
            fornitore.title = title
            user.email = email
            user.save()
            fornitore.save()
            messages.success(request, "Il tuo profilo è stato aggiornato con successo.")
        else:
            messages.error(request, "Tutti i campi sono obbligatori.")
    # Passa i dati al template
    context = {
        'fornitore': fornitore,
        'user':user
    }
    return render(request, 'useradmin/fornitore-page.html', context)

def fornitore_update(request):
    # Recupera il fornitore associato all'utente autenticato
    fornitore = Fornitore.objects.get(user=request.user)

    if request.method == "POST":
        # Popola il form con i dati inviati dal POST
        form = FornitoreForm(request.POST, request.FILES, instance=fornitore)
        if form.is_valid():
            # Salva i dati del fornitore
            fornitore_save = form.save(commit=False)
            fornitore_save.user = request.user
            fornitore_save.save()
            messages.success(request, "Il tuo profilo è stato aggiornato con successo.")
            return redirect("useradmin:fornitore-view")
        else:
            messages.error(request, "Si è verificato un errore durante l'aggiornamento del profilo.")
    else:
        # Crea un form precompilato con i dati esistenti
        form = FornitoreForm(instance=fornitore)

    # Passa il form al template
    context = {
        'form': form,
        'fornitore': fornitore
    }
    return render(request, 'useradmin/fornitore-edit.html', context)