# Create your views here.

from django.shortcuts import render
from django.http import HttpResponseRedirect
from all.models import Target, Method, Model, Refinement, ScoringFunction, Score
from django.core.urlresolvers import reverse
from all.forms import model_select_form
from all.extract import extract_interactions
import re

def target(request):
	#page with target table
        context = {'pdb_url':"http://www.rcsb.org/pdb/explore/explore.do?structureId="}
        return insert_form_and_go(request, 'all/target.html', context)

def target_info(request, name):
	#details on a particular target
	target = Target.objects.get(name=name)
	interactions = extract_interactions('all/static/bench_contacts/'+target.name+'_caprifit-contacts.out',False)
	#unbound interface residues and contacts inputted as empty to avoid drawing them (may change this)
        context = {'target':target,'ref_draw_5A_contacts':interactions['ref_draw_5A_contacts'],'ref_int_5A_residues':interactions['ref_int_5A_residues'],'ref_int_10A_residues':interactions['ref_int_10A_residues'],'inp_draw_5A_contacts':"",'inp_int_5A_residues':"",'inp_int_10A_residues':""}
        return insert_form_and_go(request, 'all/target_info.html', context)

def search(request):
	#home/search page
	return insert_form_and_go(request,'all/search.html',{})

def summary(request,target):
	#summary page
	#get data for I-RMSD comparison graph
	target_irmsds = []
	best_model_irmsds = []
	target_names = []
	target_difficulties = []
	for each in Target.objects.all():
		try:
			ordered_models = Model.objects.filter(target__name=each.name).order_by('i_rmsd')
			best_model_irmsds.append(ordered_models[0].i_rmsd)
			target_names.append(each.name)
			target_irmsds.append(each.i_rmsd)
			target_difficulties.append(each.difficulty)
		except:
			print(each.name)

	#get data for method comparison graph
	methods = []
	irmsd_by_method = []
	
	#averages across all targets need only be calculated once - here temporarily
	average_irmsds = [5.20,12.68,2.78,5.75,5.75,6.44,6.21,7.54,9.02]

	for each in Method.objects.all():
		methods.append(each.name)
		try:
			ordered_models = Model.objects.filter(target__name=target,method__name=each.name).order_by('i_rmsd')
			irmsd_by_method.append(ordered_models[0].i_rmsd)
		except:
			irmsd_by_method.append(0)
			print(each.name)

	context = {'target_names':target_names,'target_irmsds':target_irmsds,'best_model_irmsds':best_model_irmsds,'target_difficulties':target_difficulties,'target_choice':target,'methods':methods,'irmsd_by_method':irmsd_by_method,'average_irmsds':average_irmsds}
	return insert_form_and_go(request,'all/summary.html',context)

def model_select(request, target, method, refinement, i_rmsd_threshold, l_rmsd_threshold, r_rmsd_threshold, fnat_threshold):
	i_rmsd_threshold = float(re.sub('-', '.', i_rmsd_threshold))
	l_rmsd_threshold = float(re.sub('-', '.', l_rmsd_threshold))
	r_rmsd_threshold = float(re.sub('-', '.', r_rmsd_threshold))
	fnat_threshold = float(re.sub('-', '.', fnat_threshold))
#	results = Model.objects.filter(target__name=target, method__name=method, refinement__name=refinement, i_rmsd__lte=i_rmsd_threshold)
	if target not in ['All', 'Rigid', 'Medium', 'Difficult']:
		results = Model.objects.filter(target__name=target)
	elif target != 'All':
		results = Model.objects.filter(target__difficulty=target)
	else:
		results = Model.objects.all()
	if i_rmsd_threshold != 0:
		results = results.filter(i_rmsd__lte=i_rmsd_threshold)
	if l_rmsd_threshold != 0:
		results = results.filter(l_rmsd__lte=l_rmsd_threshold)
	if r_rmsd_threshold != 0:
		results = results.filter(r_rmsd__lte=r_rmsd_threshold)
	if fnat_threshold != 0:
		results = results.filter(fnat__gte=fnat_threshold)
	if method != 'All':
		results = results.filter(method__name=method)
	if refinement != 'All':
		results = results.filter(refinement__name=refinement)

	context = {'results':results}
	return insert_form_and_go(request, 'all/model_select.html', context)

def scoring(request, scorer, target):
	#comparison of scoring functions
	model_irmsds = []
	scores = []
	model_ids = []
	model_methods = []

	subset = Score.objects.filter(model__target__name=target,scoring_function__name=scorer)
	for each in subset:
		try:
			model_irmsds.append(each.model.i_rmsd)
			scores.append(each.score)
			model_ids.append(each.model.id)
			model_methods.append(each.model.method.name)
		except:
			print('error')

	context = {'target_names':Target.objects.values_list('name',flat=True),'scorer_names':ScoringFunction.objects.values_list('name',flat=True),'method_names':Method.objects.values_list('name',flat=True),'target_choice':target,'scorer_choice':scorer,'model_irmsds':model_irmsds,'scores':scores,'model_ids':model_ids,'model_methods':model_methods}
	return insert_form_and_go(request, 'all/scoring.html', context)

def model(request, id):
	#details on a particular model
        model = Model.objects.get(id=id)

	#get chain information to allow visualisation of receptor/ligand separately
	model_rec_chains = "*:"+"/3.1 or *:".join(list(model.target.receptor_bound_chain))+"/3.1"
	model_lig_chains = "*:"+"/3.1 or *:".join(list(model.target.ligand_bound_chain))+"/3.1"

	interactions = extract_interactions('all/static/1ZM4_cluspro-balanced_nothing_1_caprifit-contacts.out',True)
        context = {'model':model,'model_rec_chains':model_rec_chains,'model_lig_chains':model_lig_chains,'ref_draw_5A_contacts':interactions['ref_draw_5A_contacts'],'ref_int_5A_residues':interactions['ref_int_5A_residues'],'ref_int_10A_residues':interactions['ref_int_10A_residues'],'inp_draw_5A_contacts':interactions['inp_draw_5A_contacts'],'inp_int_5A_residues':interactions['inp_int_5A_residues'],'inp_int_10A_residues':interactions['inp_int_10A_residues']}
        return insert_form_and_go(request, 'all/model.html', context)

def method(request):
	#summary table of docking methods
	return insert_form_and_go(request, 'all/method.html', {})

def refinement(request):
	#information on the effect of refinement
	#for the minute constructs a graph for ZDock v ZDock/FiberDock performance for one target
	no_ref_irmsds = []
	improvements = []
	ref_model_ids = []
	for i in range(500):
		no_ref_irmsds.append(Model.objects.get(target__name='1ACB',method__name='ZDOCK',number=i+1,refinement__name='Nothing').i_rmsd)
		improvements.append(Model.objects.get(target__name='1ACB',method__name='ZDOCK',number=i+1,refinement__name='FiberDock').i_rmsd - Model.objects.get(target__name='1ACB',method__name='ZDOCK',number=i+1,refinement__name='Nothing').i_rmsd)
		ref_model_ids.append(Model.objects.get(target__name='1ACB',method__name='ZDOCK',number=i+1,refinement__name='FiberDock').id)
	context = {'no_ref_irmsds':no_ref_irmsds,'improvements':improvements,'ref_model_ids':ref_model_ids}
	return insert_form_and_go(request, 'all/refinement.html', context)

def about(request):
	#about page
	return insert_form_and_go(request, 'all/about.html', {})

def insert_form_and_go(request,template,context):
	#inserts the model select form onto every page and renders the page
	if request.method == 'GET':
		form = model_select_form()
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
			return HttpResponseRedirect(reverse('model_select',kwargs={'target':target,'method':method,'refinement':refinement, 'i_rmsd_threshold':i_rmsd_threshold, 'l_rmsd_threshold':l_rmsd_threshold, 'r_rmsd_threshold':r_rmsd_threshold, 'fnat_threshold':fnat_threshold}))
	context['Target'] = Target.objects.all()
	context['Rigid'] = Target.objects.filter(difficulty='Rigid')
	context['Medium'] = Target.objects.filter(difficulty='Medium')
	context['Difficult'] = Target.objects.filter(difficulty='Difficult')
	context['form'] = form
	return render(request, template, context)















