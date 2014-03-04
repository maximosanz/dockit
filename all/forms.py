from django import forms
from all.models import Target
from all.models import Method
from all.models import Refinement

class model_select_form(forms.Form):
        target_options = [['All', 'All targets'],['Rigid', 'All rigid targets']]
        for complex in Target.objects.filter(difficulty='Rigid'):
                target_options.append([complex.name,complex.name])
	target_options.append(['Medium', 'All medium targets'])
	for complex in Target.objects.filter(difficulty='Medium'):
                target_options.append([complex.name,complex.name])
	target_options.append(['Difficult', 'All difficult targets'])
	for complex in Target.objects.filter(difficulty='Difficult'):
                target_options.append([complex.name,complex.name])
        target = forms.ChoiceField(choices=target_options)
	method_options = [['All', 'All methods']]
	for m in Method.objects.all():
		method_options.append([m.name,m.name])
        method = forms.ChoiceField(choices=method_options)
	refinement_options = [['All', 'All refinements']]
	for r in Refinement.objects.all():
		refinement_options.append([r.name,r.name])
	refinement = forms.ChoiceField(choices=refinement_options)
	i_rmsd_threshold = forms.DecimalField(label='Maximum I-RMSD', initial=0)
	l_rmsd_threshold = forms.DecimalField(label='Maximum L-RMSD', initial=0)
	r_rmsd_threshold = forms.DecimalField(label='Maximum R-RMSD', initial=0)
	fnat_threshold = forms.DecimalField(label='Minimum fraction of natural contacts', initial=0)
