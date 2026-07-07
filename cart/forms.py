from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES, coerce=int, initial=1,
        widget=forms.Select(attrs={'class': 'border rounded px-2 py-1 w-20'})
    )
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
