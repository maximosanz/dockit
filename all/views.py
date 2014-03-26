# Create your views here.

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from all.models import Target, Method, Model, Refinement, ScoringFunction, Score
from django.core.urlresolvers import reverse
from all.forms import model_select_form
from all.extract import extract_interactions
from django.contrib.staticfiles.templatetags.staticfiles import static
import re
from django.template import add_to_builtins
add_to_builtins('djangojs.templatetags.js')

def target(request):
	#page with target table
        context = {'pdb_url':"http://www.rcsb.org/pdb/explore/explore.do?structureId="}
        return insert_form_and_go(request, 'all/target.html', context)

def target_info(request, name):
	#details on a particular target
	target = Target.objects.get(name=name)
	dasa = target.asa_rl_b - target.asa_c_b
	#category of target
	cat_dict={'E':'Enzyme/Inhibitor or Enzyme/substrate','A':'Antibody/Antigen','O':'Others','AB':'Antigen/Bound antibody'}
	target_dict=target.__dict__
	complete_cat=cat_dict[target_dict['category']]
	#need to change from absolute filepath
	interactions = extract_interactions('/project/data/dockit/static/bench_contacts/'+target.name+'_caprifit-contacts.out',False)
	#interactions = extract_interactions(static('bench_contacts/'+target.name+'_caprifit-contacts.out'),False)
	file_names = {'rb':'benchmarks/'+target.name+'_r_b.pdb','lb':'benchmarks/'+target.name+'_l_b.pdb','ru':'benchmarks/'+target.name+'_r_u_cleanedup.pdb','lu':'benchmarks/'+target.name+'_l_u_cleanedup.pdb'}
	#unbound interface residues and contacts inputted as empty to avoid drawing them (may change this)
        context = {'target':target,'dasa':dasa,'file_names':file_names,'ref_draw_5A_contacts':interactions['ref_draw_5A_contacts'],'ref_int_5A_residues':interactions['ref_int_5A_residues'],'ref_int_10A_residues':interactions['ref_int_10A_residues'],'inp_draw_5A_contacts':interactions['inp_draw_5A_contacts'],'inp_int_5A_residues':interactions['inp_int_5A_residues'],'inp_int_10A_residues':interactions['inp_int_10A_residues'],'pdb_url':"http://www.rcsb.org/pdb/explore/explore.do?structureId=",'complete_cat':complete_cat}
        return insert_form_and_go(request, 'all/target_info.html', context)

def search(request):
	#home/search page
	return insert_form_and_go(request,'all/search.html',{})

def summary(request,target):
	#summary page
	#get data for I-RMSD comparison graph
	target_difficulty = Target.objects.get(name=target).difficulty
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

	#get data for method comparison graphs
	methods = []
	irmsd_by_method = []
	acceptable_by_method_500 = []
	acceptable_by_method_100 = []
	acceptable_by_method_10 = []
	medium_by_method_500 = []
	medium_by_method_100 = []
	medium_by_method_10 = []
	high_by_method_500 = []
	high_by_method_100 = []
	high_by_method_10 = []

	models = Model.objects.filter(target__name=target).values('id','number','method__name','refinement__name','i_rmsd','capri_ev','capri_valid')
	best_irmsd_model_by_method = []
	
	#produces a readable name for method and refinement
	def get_field_name(method,refinement):
		if (refinement == '-' or refinement == 'Rosetta'):
			field_name = method
		else:
			field_name = method + ' then ' + refinement
		return field_name
	
	#construct method and refinement array
	for model in models:
		field_name = get_field_name(model['method__name'],model['refinement__name'])
		if field_name not in methods:
			methods.append(field_name)
			irmsd_by_method.append(0)
			best_irmsd_model_by_method.append(0)
			acceptable_by_method_500.append(0)
			acceptable_by_method_100.append(0)
			acceptable_by_method_10.append(0)
			medium_by_method_500.append(0)
			medium_by_method_100.append(0)
			medium_by_method_10.append(0)
			high_by_method_500.append(0)
			high_by_method_100.append(0)
			high_by_method_10.append(0)

	#construct arrays of values
	for model in models:
		field_name = get_field_name(model['method__name'],model['refinement__name'])
		for i in range(len(methods)):
			if (methods[i] == field_name and model['capri_valid'] == 1):
				if (model['capri_ev'] == 1):
					if (model['number'] <= 10):
						acceptable_by_method_500[i] += 1
						acceptable_by_method_100[i] += 1
						acceptable_by_method_10[i] += 1
					elif (model['number'] <= 100):
						acceptable_by_method_500[i] += 1
						acceptable_by_method_100[i] += 1
					elif (model['number'] <= 500):
						acceptable_by_method_500[i] += 1
				elif (model['capri_ev'] == 2):
					if (model['number'] <= 10):
						medium_by_method_500[i] += 1
						medium_by_method_100[i] += 1
						medium_by_method_10[i] += 1
					elif (model['number'] <= 100):
						medium_by_method_500[i] += 1
						medium_by_method_100[i] += 1
					elif (model['number'] <= 500):
						medium_by_method_500[i] += 1
				elif (model['capri_ev'] == 3):
					if (model['number'] <= 10):
						high_by_method_500[i] += 1
						high_by_method_100[i] += 1
						high_by_method_10[i] += 1
					elif (model['number'] <= 100):
						high_by_method_500[i] += 1
						high_by_method_100[i] += 1
					elif (model['number'] <= 500):
						high_by_method_500[i] += 1
				if (irmsd_by_method[i] == 0 or irmsd_by_method[i] > model['i_rmsd']):
					if (model['capri_valid'] == 1):
						irmsd_by_method[i] = model['i_rmsd']
						best_irmsd_model_by_method[i] = model['id']
				break
	
	at_least_one = False
	at_least_one_no_cluspro = False
	for method in acceptable_by_method_500:
		if (method > 0):
			at_least_one = True;
			if not re.match("cluspro", methods[acceptable_by_method_500.index(method)], re.IGNORECASE):
				at_least_one_no_cluspro = True
				break

	context = {'target_names':target_names,'target_irmsds':target_irmsds,'best_model_irmsds':best_model_irmsds,'target_difficulties':target_difficulties,'target_choice':target,'target_difficulty':target_difficulty.lower(),'methods':methods,'irmsd_by_method':irmsd_by_method,'acceptable_by_method_500':acceptable_by_method_500,'acceptable_by_method_100':acceptable_by_method_100,'acceptable_by_method_10':acceptable_by_method_10,'medium_by_method_500':medium_by_method_500,'medium_by_method_100':medium_by_method_100,'medium_by_method_10':medium_by_method_10,'high_by_method_500':high_by_method_500,'high_by_method_100':high_by_method_100,'high_by_method_10':high_by_method_10,'at_least_one':at_least_one,'at_least_one_no_cluspro':at_least_one_no_cluspro,'best_irmsd_model_by_method':best_irmsd_model_by_method}
	return insert_form_and_go(request,'all/summary.html',context)

def model_select(request, target, method, refinement, i_rmsd_threshold, l_rmsd_threshold, r_rmsd_threshold, fnat_threshold, rank_str, bypass):
	if bypass=='0':
		bypass =False
	else:
		bypass=True
	i_rmsd_threshold = float(re.sub('-', '.', i_rmsd_threshold))
	l_rmsd_threshold = float(re.sub('-', '.', l_rmsd_threshold))
	r_rmsd_threshold = float(re.sub('-', '.', r_rmsd_threshold))
	fnat_threshold = float(re.sub('-', '.', fnat_threshold))
	if target not in ['All', 'Rigid', 'Medium', 'Difficult']:
		results = Model.objects.filter(target__name=target)
	elif target != 'All':
		results = Model.objects.filter(target__difficulty=target)
	else:
		results = Model.objects.all()
	possible_ranks=['Incorrect','Acceptable','Medium','High','Removed']
	if rank_str != "1":
		rank_filters=[]
		for i in range(4):
			if rank_str[i]=="1":
				rank_filters.append(i)
		if rank_str[4] == "0":
			results = results.filter(Q(capri_ev__in=rank_filters) & Q(capri_valid=1))
		else:
			results = results.filter(Q(capri_ev__in=rank_filters) | Q(capri_valid=0))
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
	count=results.count()
	if count>1000 and not bypass:
		context = {'results':results, 'count':count}
		return HttpResponseRedirect(reverse('refine_search',kwargs={'target':target,'method':method,'refinement':refinement, 'i_rmsd_t':i_rmsd_threshold, 'l_rmsd_t':l_rmsd_threshold, 'r_rmsd_t':r_rmsd_threshold, 'fnat_t':fnat_threshold, 'rank_str':rank_str,'count':count}))
	else:
		results=results.values('id','number','i_rmsd','l_rmsd','r_rmsd','fnat','i_l_rmsd','method__name','refinement__name','target__name','target__difficulty','target__complex','target__ligand','target__receptor','capri_ev','capri_valid','no_clashes','asa_c','asa_rl','score__scoring_function__name','score__score')
		if not results:
			return insert_form_and_go(request, 'all/noresults.html', {})
		else:
			final_results=[]
			capri_ranks=['Incorrect','Acceptable','Medium','High']
			j=0
			for i in range(count):
				final_results.append(results[i+j])
				model=final_results[i]
				model['method__name_lower']=model['method__name'].lower()
				if (model['refinement__name'] == '-'):
					model['refinement__name_lower']='nothing'
				else:
					model['refinement__name_lower']=model['refinement__name'].lower()
				model['target__difficulty_lower']=model['target__difficulty'].lower()
				model['dasa']=model['asa_rl']-model['asa_c']
				if model['capri_valid'] == 0:
					model['capri_rank']='Removed'
				else:
					model['capri_rank']=capri_ranks[model['capri_ev']]
				for sc_f in ScoringFunction.objects.all().values('name'):
					final_results[i][sc_f['name'].lower()+'_score']='Not scored'
				sc_f=model['score__scoring_function__name']
				cur_id=final_results[i]['id']
				cur_i=i
				if sc_f != None:
					while i+j<len(results) and results[i+j]['id']==cur_id:
						sc_f=results[i+j]['score__scoring_function__name']
						if results[i+j]['score__score'] == None:
							final_results[cur_i][sc_f.lower()+'_score']='Unable to score model'
						else:
							final_results[cur_i][sc_f.lower()+'_score']=results[i+j]['score__score']
						if i != cur_i:
							j+=1					
						i+=1
			context = {'results':final_results}				
			if target not in ['All', 'Rigid', 'Medium', 'Difficult']:
				return HttpResponseRedirect(reverse('target_models',kwargs={'name':target,'method':method,'refinement':refinement, 'i_rmsd_threshold':i_rmsd_threshold, 'l_rmsd_threshold':l_rmsd_threshold, 'r_rmsd_threshold':r_rmsd_threshold, 'fnat_threshold':fnat_threshold, 'rank_str':rank_str}))
			else:
				return insert_form_and_go(request, 'all/model_select.html', context)


def scoring(request, scorer, target, cutoff):
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

	context = {'target_names':Target.objects.values_list('name',flat=True),'scorer_names':ScoringFunction.objects.values_list('name',flat=True),'method_names':Method.objects.values_list('name',flat=True),'target_choice':target,'scorer_choice':scorer,'model_irmsds':model_irmsds,'scores':scores,'model_ids':model_ids,'model_methods':model_methods,'cutoff':cutoff}
	return insert_form_and_go(request, 'all/scoring.html', context)

def model(request, id):
	#details on a particular model
        model = Model.objects.get(id=id)
	
	dasa = model.asa_rl - model.asa_c
	
	if (model.refinement.name == "-"):
		refinement = "nothing"
	else:
		refinement = model.refinement.name.lower()

	file_names = {'rb':'benchmarks/'+model.target.name+'_r_b.pdb','lb':'benchmarks/'+model.target.name+'_l_b.pdb','model':'results/'+model.method.name.lower()+'/'+refinement+'/'+model.target.difficulty.lower()+'/'+model.target.name+'/'+model.target.name+'_'+model.method.name.lower()+'_'+refinement+'_'+str(model.number)+'.pdb-'+model.target.receptor_bound_chain+'-fitted'}

	#get chain information to allow visualisation of receptor/ligand separately
	model_rec_chains = "*:"+"/3.1 or *:".join(list(model.target.receptor_bound_chain))+"/3.1"
	model_lig_chains = "*:"+"/3.1 or *:".join(list(model.target.ligand_bound_chain))+"/3.1"

	#needs changing from absolute filepath
	interactions = extract_interactions('/project/data/dockit/static/results/'+model.method.name.lower()+'/'+refinement+'/'+model.target.difficulty.lower()+'/'+model.target.name+'/'+model.target.name+'_'+model.method.name.lower()+'_'+refinement+'_'+str(model.number)+'_caprifit-contacts.out',True)

	def get_score(scorer):
		if (len(Score.objects.filter(model__id=id,scoring_function__name=scorer)) > 0):
			return Score.objects.get(model__id=id,scoring_function__name=scorer).score
		else:
			return '-'

	zrank_score = get_score('ZRANK')
	zrank2_score = get_score('ZRANK2')
	pisa_score = get_score('PISA')

        context = {'model':model,'pdb_url':"http://www.rcsb.org/pdb/explore/explore.do?structureId=",'dasa':dasa,'file_names':file_names,'model_rec_chains':model_rec_chains,'model_lig_chains':model_lig_chains,'ref_draw_5A_contacts':interactions['ref_draw_5A_contacts'],'ref_int_5A_residues':interactions['ref_int_5A_residues'],'ref_int_10A_residues':interactions['ref_int_10A_residues'],'inp_draw_5A_contacts':interactions['inp_draw_5A_contacts'],'inp_int_5A_residues':interactions['inp_int_5A_residues'],'inp_int_10A_residues':interactions['inp_int_10A_residues'],'zrank_score':zrank_score,'zrank2_score':zrank2_score,'pisa_score':pisa_score}
        return insert_form_and_go(request, 'all/model.html', context)

def target_models(request, name, method, refinement, i_rmsd_threshold, l_rmsd_threshold, r_rmsd_threshold, fnat_threshold, rank_str):
	#table with info and JSmol display of all models produced for a target
	i_rmsd_threshold = float(re.sub('-', '.', i_rmsd_threshold))
	l_rmsd_threshold = float(re.sub('-', '.', l_rmsd_threshold))
	r_rmsd_threshold = float(re.sub('-', '.', r_rmsd_threshold))
	fnat_threshold = float(re.sub('-', '.', fnat_threshold))
	target = Target.objects.get(name=name)

	rec_chains = list(target.receptor_bound_chain)
	hide_rec_chains = ""
	for i in range(len(rec_chains)):
		hide_rec_chains += " hide hidden or (chain="+rec_chains[i]+");"
	hide_rec_chains = hide_rec_chains[1:-1]

	results = Model.objects.filter(target__name=name)
	if rank_str != "1":
		rank_filters=[]
		for i in range(4):
			if rank_str[i]=="1":
				rank_filters.append(i)
		if rank_str[4] == "0":
			results = results.filter(Q(capri_ev__in=rank_filters) & Q(capri_valid=1))
		else:
			results = results.filter(Q(capri_ev__in=rank_filters) | Q(capri_valid=0))
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
	count=results.count()
	results=results.values('id','i_rmsd','l_rmsd','r_rmsd','fnat','i_l_rmsd','method__name','refinement__name','target__name','target__difficulty','number','target__receptor_bound_chain','capri_ev','capri_valid','no_clashes','asa_c','asa_rl','score__scoring_function__name','score__score')
	if not results:
		return insert_form_and_go(request, 'all/noresults.html', {})
	else:
		final_results=[]
		capri_ranks=['Incorrect','Acceptable','Medium','High']
		j=0
		for i in range(count):
			final_results.append(results[i+j])
			model=final_results[i]
			model['method__name_lower']=model['method__name'].lower()
			if (model['refinement__name'] == '-'):
				model['refinement__name_lower']='nothing'
			else:
				model['refinement__name_lower']=model['refinement__name'].lower()
			model['target__difficulty_lower']=model['target__difficulty'].lower()
			model['dasa']=model['asa_rl']-model['asa_c']
			if model['capri_valid'] == 0:
				model['capri_rank']='Removed'
			else:
				model['capri_rank']=capri_ranks[model['capri_ev']]
			for sc_f in ScoringFunction.objects.all().values('name'):
				final_results[i][sc_f['name'].lower()+'_score']='Not scored'
			sc_f=model['score__scoring_function__name']
			cur_id=final_results[i]['id']
			cur_i=i
			if sc_f != None:
				while i+j<len(results) and results[i+j]['id']==cur_id:
					sc_f=results[i+j]['score__scoring_function__name']
					if results[i+j]['score__score'] == None:
						final_results[cur_i][sc_f.lower()+'_score']='Unable to score model'
					else:
						final_results[cur_i][sc_f.lower()+'_score']=results[i+j]['score__score']
					if i != cur_i:
						j+=1					
					i+=1

	#get data for method comparison graphs
	target_difficulty = target.difficulty
	methods = []
	irmsd_by_method = []
	acceptable_by_method_500 = []
	acceptable_by_method_100 = []
	acceptable_by_method_10 = []
	medium_by_method_500 = []
	medium_by_method_100 = []
	medium_by_method_10 = []
	high_by_method_500 = []
	high_by_method_100 = []
	high_by_method_10 = []
	best_irmsd_model_by_method = []

	models = Model.objects.filter(target__name=name).values('id','number','method__name','refinement__name','i_rmsd','capri_ev','capri_valid')
	
	#produces a readable name for method and refinement
	def get_field_name(method,refinement):
		if (refinement == '-' or refinement == 'Rosetta'):
			field_name = method
		else:
			field_name = method + ' then ' + refinement
		return field_name
	
	#construct method and refinement array
	for model in models:
		field_name = get_field_name(model['method__name'],model['refinement__name'])
		if field_name not in methods:
			methods.append(field_name)
			irmsd_by_method.append(0)
			acceptable_by_method_500.append(0)
			acceptable_by_method_100.append(0)
			acceptable_by_method_10.append(0)
			medium_by_method_500.append(0)
			medium_by_method_100.append(0)
			medium_by_method_10.append(0)
			high_by_method_500.append(0)
			high_by_method_100.append(0)
			high_by_method_10.append(0)
			best_irmsd_model_by_method.append(0)

	#construct arrays of values
	for model in models:
		field_name = get_field_name(model['method__name'],model['refinement__name'])
		for i in range(len(methods)):
			if (methods[i] == field_name and model['capri_valid'] == 1):
				if (model['capri_ev'] == 1):
					if (model['number'] <= 10):
						acceptable_by_method_500[i] += 1
						acceptable_by_method_100[i] += 1
						acceptable_by_method_10[i] += 1
					elif (model['number'] <= 100):
						acceptable_by_method_500[i] += 1
						acceptable_by_method_100[i] += 1
					elif (model['number'] <= 500):
						acceptable_by_method_500[i] += 1
				elif (model['capri_ev'] == 2):
					if (model['number'] <= 10):
						medium_by_method_500[i] += 1
						medium_by_method_100[i] += 1
						medium_by_method_10[i] += 1
					elif (model['number'] <= 100):
						medium_by_method_500[i] += 1
						medium_by_method_100[i] += 1
					elif (model['number'] <= 500):
						medium_by_method_500[i] += 1
				elif (model['capri_ev'] == 3):
					if (model['number'] <= 10):
						high_by_method_500[i] += 1
						high_by_method_100[i] += 1
						high_by_method_10[i] += 1
					elif (model['number'] <= 100):
						high_by_method_500[i] += 1
						high_by_method_100[i] += 1
					elif (model['number'] <= 500):
						high_by_method_500[i] += 1
				if (irmsd_by_method[i] == 0 or irmsd_by_method[i] > model['i_rmsd']):
					if (model['capri_valid'] == 1):
						irmsd_by_method[i] = model['i_rmsd']
						best_irmsd_model_by_method[i] = model['id']
				break
	
	at_least_one = False
	at_least_one_no_cluspro = False
	for method in acceptable_by_method_500:
		if (method > 0):
			at_least_one = True;
			if not re.match("cluspro", methods[acceptable_by_method_500.index(method)], re.IGNORECASE):
				at_least_one_no_cluspro = True
				break

	context = {'target':target, 'hide_rec_chains':hide_rec_chains, 'results':final_results,'target_difficulty':target_difficulty.lower(),'methods':methods,'irmsd_by_method':irmsd_by_method,'acceptable_by_method_500':acceptable_by_method_500,'acceptable_by_method_100':acceptable_by_method_100,'acceptable_by_method_10':acceptable_by_method_10,'medium_by_method_500':medium_by_method_500,'medium_by_method_100':medium_by_method_100,'medium_by_method_10':medium_by_method_10,'high_by_method_500':high_by_method_500,'high_by_method_100':high_by_method_100,'high_by_method_10':high_by_method_10,'at_least_one':at_least_one,'at_least_one_no_cluspro':at_least_one_no_cluspro,'best_irmsd_model_by_method':best_irmsd_model_by_method}
	return insert_form_and_go(request, 'all/target_models.html', context)
	

def method(request):
	#summary table of docking methods
	return insert_form_and_go(request, 'all/method.html', {})

def refinement(request,method,refinement,target,cutoff):
	#information on the effect of refinement
	#for the minute constructs a graph for ZDock v ZDock/FiberDock performance for one target
	no_ref_irmsds = []
	improvements = []
	ref_model_ids = []

	models = Model.objects.filter(target__name=target,method__name=method,irmsd__lte=cutoff).values('id','refinement__name','i_rmsd','number')

	for i in range(500):
		for model in models:
			if (model.number == i and model.refinement=refinement):
				refined_irmsd = model.i_rmsd
			if (model.number == i and model.refinement='-'):
				no_ref_irmsd = model.i_rmsd
		improvements.append(refined_irmsd - no_ref_irmsd)


	for i in range(500):
		no_ref_irmsds.append(Model.objects.get(target__name=target,method__name=method,number=i+1,refinement__name='-').i_rmsd)
		improvements.append(Model.objects.get(target__name=target,method__name=method,number=i+1,refinement__name=refinement).i_rmsd - Model.objects.get(target__name=target,method__name=method,number=i+1,refinement__name='-').i_rmsd)
		ref_model_ids.append(Model.objects.get(target__name=target,method__name=method,number=i+1,refinement__name=refinement).id)

	context = {'method':method,'refinement':refinement,'target':target,'no_ref_irmsds':no_ref_irmsds,'improvements':improvements,'ref_model_ids':ref_model_ids,'target_names':Target.objects.values_list('name',flat=True),'method_names':Method.objects.values_list('name',flat=True),'refinement_names':Refinement.objects.values_list('name',flat=True),'cutoff':cutoff}

	return insert_form_and_go(request, 'all/refinement.html', context)

def about(request):
	#about page
	return insert_form_and_go(request, 'all/about.html', {})

def noresults(request):
	#reached if no results match a search
	return insert_form_and_go(request, 'all/noresults.html', {})

def refine_search(request, target, method, refinement, i_rmsd_t, l_rmsd_t, r_rmsd_t, fnat_t, rank_str, count):
	#reached if too many results to display

	i_rmsd_threshold = float(re.sub('-', '.', i_rmsd_t))
	if i_rmsd_threshold == 0.0:
		i_rmsd_threshold=None
	l_rmsd_threshold = float(re.sub('-', '.', l_rmsd_t))
	if l_rmsd_threshold == 0.0:
		l_rmsd_threshold=None
	r_rmsd_threshold = float(re.sub('-', '.', r_rmsd_t))
	if r_rmsd_threshold == 0.0:
		r_rmsd_threshold=None
	fnat_threshold = float(re.sub('-', '.', fnat_t))
	if fnat_threshold == 0.0:
		fnat_threshold=None
	possible_ranks=['Incorrect','Acceptable','Medium','High','Removed']
	if rank_str != "1":
		capri_ranks=[]
		for i in range(5):
			if rank_str[i]=="1":
				capri_ranks.append(possible_ranks[i])
	else:
		capri_ranks=['All_ranks']
#	temp="csv/"+target+"_models.csv"
	if request.method == 'GET':
		initiated_form = model_select_form(initial={'target':target,'method':method,'refinement':refinement,'i_rmsd_threshold':i_rmsd_threshold,'l_rmsd_threshold':l_rmsd_threshold,'r_rmsd_threshold':r_rmsd_threshold,'fnat_threshold':fnat_threshold,'capri_rank':capri_ranks})
		context={'count':count,'initiated_form':initiated_form,'target':target,'method':method,'refinement':refinement,'i_rmsd_threshold':i_rmsd_t,'l_rmsd_threshold':l_rmsd_t,'r_rmsd_threshold':r_rmsd_t,'fnat_threshold':fnat_t,'rank_str':rank_str}
		return insert_form_and_go(request, 'all/refine_search.html', context)

	else:
		initiated_form = model_select_form(request.POST)
		if initiated_form.is_valid():
		        target = initiated_form.cleaned_data['target']
		        method = initiated_form.cleaned_data['method']
			refinement = initiated_form.cleaned_data['refinement']
			capri_rank = initiated_form.cleaned_data['capri_rank']
			i_rmsd_t = str(initiated_form.cleaned_data['i_rmsd_threshold'])
			i_rmsd_threshold = re.sub('\.', '-', i_rmsd_t)
			if i_rmsd_threshold == "None":
				i_rmsd_threshold = "0"
			l_rmsd_t = str(initiated_form.cleaned_data['l_rmsd_threshold'])
			l_rmsd_threshold = re.sub('\.', '-', l_rmsd_t)
			if l_rmsd_threshold == "None":
				l_rmsd_threshold = "0"
			r_rmsd_t = str(initiated_form.cleaned_data['r_rmsd_threshold'])
			r_rmsd_threshold = re.sub('\.', '-', r_rmsd_t)
			if r_rmsd_threshold == "None":
				r_rmsd_threshold = "0"
			fnat_t = str(initiated_form.cleaned_data['fnat_threshold'])
			fnat_threshold = re.sub('\.', '-', fnat_t)
			if fnat_threshold == "None":
				fnat_threshold = "0"
			possible_ranks=['Incorrect','Acceptable','Medium','High','Removed']
			if "All_ranks" in capri_rank:
				rank_str='1'
			else:
				rank_str=""
				for option in possible_ranks:
					if option in capri_rank:
						rank_str+="1"
					else:
						rank_str+="0"

			return HttpResponseRedirect(reverse('model_select',kwargs={'target':target,'method':method,'refinement':refinement, 'i_rmsd_threshold':i_rmsd_threshold, 'l_rmsd_threshold':l_rmsd_threshold, 'r_rmsd_threshold':r_rmsd_threshold, 'fnat_threshold':fnat_threshold, 'rank_str':rank_str, 'bypass':'0'}))




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
			capri_rank = form.cleaned_data['capri_rank']
			i_rmsd_t = str(form.cleaned_data['i_rmsd_threshold'])
			i_rmsd_threshold = re.sub('\.', '-', i_rmsd_t)
			if i_rmsd_threshold == "None":
				i_rmsd_threshold = "0"
			l_rmsd_t = str(form.cleaned_data['l_rmsd_threshold'])
			l_rmsd_threshold = re.sub('\.', '-', l_rmsd_t)
			if l_rmsd_threshold == "None":
				l_rmsd_threshold = "0"
			r_rmsd_t = str(form.cleaned_data['r_rmsd_threshold'])
			r_rmsd_threshold = re.sub('\.', '-', r_rmsd_t)
			if r_rmsd_threshold == "None":
				r_rmsd_threshold = "0"
			fnat_t = str(form.cleaned_data['fnat_threshold'])
			fnat_threshold = re.sub('\.', '-', fnat_t)
			if fnat_threshold == "None":
				fnat_threshold = "0"
			possible_ranks=['Incorrect','Acceptable','Medium','High','Removed']
			if "All_ranks" in capri_rank:
				rank_str='1'
			else:
				rank_str=""
				for option in possible_ranks:
					if option in capri_rank:
						rank_str+="1"
					else:
						rank_str+="0"
			return HttpResponseRedirect(reverse('model_select',kwargs={'target':target,'method':method,'refinement':refinement, 'i_rmsd_threshold':i_rmsd_threshold, 'l_rmsd_threshold':l_rmsd_threshold, 'r_rmsd_threshold':r_rmsd_threshold, 'fnat_threshold':fnat_threshold, 'rank_str':rank_str, 'bypass':'0'}))
	context['Target'] = Target.objects.all()
	context['Rigid'] = Target.objects.filter(difficulty='Rigid')
	context['Medium'] = Target.objects.filter(difficulty='Medium')
	context['Difficult'] = Target.objects.filter(difficulty='Difficult')
	context['form'] = form
	return render(request, template, context)

