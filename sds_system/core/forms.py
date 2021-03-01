from django import forms


class MatchForm(forms.Form):
    trade_name = forms.CharField(label='Trade Name', max_length=100, required=False)
    supplier = forms.CharField(label='Supplier', max_length=100, required=False)


class SDSFileForm(forms.Form):
    file = forms.FileField(label='SDS File', required=False)
    url = forms.URLField(label='SDS URL', required=False)
