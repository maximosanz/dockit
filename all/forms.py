from django import forms
from all.models import Target

class model_select_form(forms.Form):
        options = []
        for complex in Target.objects.all():
                options.append([complex.name,complex.name])
        target = forms.ChoiceField(choices=options)
        method = forms.ChoiceField(choices=(('Hex','Hex'),('Rosetta','Rosetta')))
