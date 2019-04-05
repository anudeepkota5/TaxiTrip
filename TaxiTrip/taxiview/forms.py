from django import forms

class IndexForm(forms.Form):
    date = forms.CharField()
    distance = forms.CharField()
    passCountt = forms.Select()
    adate = forms.Select()
