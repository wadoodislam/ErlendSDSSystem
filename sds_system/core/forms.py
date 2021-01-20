from django import forms


class MatchForm(forms.Form):
    trade_name = forms.CharField(label='Trade Name', max_length=100)
    supplier = forms.CharField(label='Supplier', max_length=100, required=False)
