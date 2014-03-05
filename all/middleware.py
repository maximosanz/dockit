from all.forms import model_select_form
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import re

class model_search_middleware(object):
	def process_request(self,request):
		if request.method == 'GET':
			form = model_select_form()
			print('get')
		else:
			form = model_select_form(request.POST)
			if form.is_valid():
			        target = form.cleaned_data['target']
			        method = form.cleaned_data['method']
				refinement = form.cleaned_data['refinement']
				i_rmsd_t = str(form.cleaned_data['i_rmsd_threshold'])
				i_rmsd_threshold = re.sub('\.', '-', i_rmsd_t)
				l_rmsd_t = str(form.cleaned_data['l_rmsd_threshold'])
				l_rmsd_threshold = re.sub('\.', '-', l_rmsd_t)
				r_rmsd_t = str(form.cleaned_data['r_rmsd_threshold'])
				r_rmsd_threshold = re.sub('\.', '-', r_rmsd_t)
				fnat_t = str(form.cleaned_data['fnat_threshold'])
				fnat_threshold = re.sub('\.', '-', fnat_t)
				print('post')
				return HttpResponseRedirect(reverse('model_select',kwargs={'target':target,'method':method,'refinement':refinement, 'i_rmsd_threshold':i_rmsd_threshold, 'l_rmsd_threshold':l_rmsd_threshold, 'r_rmsd_threshold':r_rmsd_threshold, 'fnat_threshold':fnat_threshold}))
		request.test = 1
