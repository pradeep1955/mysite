from django import forms

from .models import Holding


class HoldingForm(forms.ModelForm):
    class Meta:
        model = Holding
        exclude = ("user",)
        widgets = {
            "purchase_date": forms.DateInput(attrs={"type": "date"}),
        }
