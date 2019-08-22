from django import forms
from .models import Call

class CallForm(forms.ModelForm):
    RULES_CHOICES = (
        ("fifo", "First In First Out (FIFO)"),
        ("lifo", "Last In Last Out (LIFO)"),
    )
    rules = forms.ChoiceField(choices=RULES_CHOICES)

    class Meta:
        model = Call
        fields = ["date", "investment_name", "capital_requirement"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].input_formats = ["%d/%m/%Y"]
