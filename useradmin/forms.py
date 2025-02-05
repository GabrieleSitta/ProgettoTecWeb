from gymapp.models import Product, Fornitore
from django import forms

# Modulo per l'aggiunta di un nuovo prodotto, includendo campi con widget personalizzati 
# per migliorare l'esperienza utente nella compilazione del modulo
class AddProductForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nome Prodotto", "class": "form-control"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Descrizione prodotto", "class": "form-control"}))
    price = forms.CharField(widget=forms.NumberInput(attrs={"placeholder": "Prezzo Vendita", "class": "form-control"}))
    stock_count = forms.CharField(widget=forms.NumberInput(attrs={"placeholder": "Quanti nello stock?", "class": "form-control"}))
    image = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control"}))
    class Meta:
        model = Product
        fields = [
            'title',
            'image',
            'description',
            'price',
            'stock_count',
            'categ_type',
            'vendor',
            'categoria'
        ]

# Modulo per la registrazione o modifica di un fornitore, includendo campi con placeholder
# per facilitare la compilazione dei dati aziendali
class FornitoreForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Nome azienda"}))
    description = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Bio"}))
    address = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Indirizzo"}))
    
    class Meta:
        model = Fornitore
        fields = ['title', 'image', 'description', 'address']