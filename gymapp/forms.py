from django import forms
from gymapp.models import ProductReview, FornitoreReview

# Definisce un modulo per la recensione di un prodotto, includendo un campo di testo con 
# un'area di input personalizzata e specificando i campi del modello ProductReview da utilizzare.
class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Scrivi qui..."}))

    class Meta:
        model = ProductReview
        fields = ['review', 'rating']

# Definisce un modulo per la recensione di un fornitore, specificando i campi del modello 
# FornitoreReview che l'utente può compilare.
class FornitoreReviewForm(forms.ModelForm):
    class Meta:
        model = FornitoreReview
        fields = ['rating', 'comment']