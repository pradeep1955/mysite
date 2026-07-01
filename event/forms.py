from django import forms

from .models import EventSchedule, Material, Task


class EventForm(forms.ModelForm):
    class Meta:
        model = EventSchedule
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
        }


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ["name", "quantity", "is_arranged", "remark"]


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["description", "due_date", "is_completed"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }
