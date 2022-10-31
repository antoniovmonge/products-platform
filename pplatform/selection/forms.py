from django import forms


class SelectionAddProductForm(forms.Form):
    override = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput
    )
