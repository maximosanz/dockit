from django.conf.urls import patterns, url
import re
from all import views

urlpatterns = patterns('',
    url(r'^$', views.search, name='search'),
    url(r'^summary_(?P<target>\w+)/$', views.summary, name='summary'),
    url(r'^target_models_(?P<name>[\S|^\_]+)_(?P<method>[\S|^\_]+)_(?P<refinement>[\S|^\_]+)_(?P<i_rmsd_threshold>[\S|^\_]+)_(?P<l_rmsd_threshold>[\S|^\_]+)_(?P<r_rmsd_threshold>[\S|^\_]+)_(?P<fnat_threshold>[\S|^\_]+)_(?P<rank_str>[\S|^\_]+)/$', views.target_models, name='target_models'),
    url(r'^target/$', views.target, name='target'),
    url(r'^target/(?P<name>\w+)/$', views.target_info, name='target_info'),
    url(r'^model_select_(?P<target>[\S|^\_]+)_(?P<method>[\S|^\_]+)_(?P<refinement>[\S|^\_]+)_(?P<i_rmsd_threshold>[\S|^\_]+)_(?P<l_rmsd_threshold>[\S|^\_]+)_(?P<r_rmsd_threshold>[\S|^\_]+)_(?P<fnat_threshold>[\S|^\_]+)_(?P<rank_str>[\S|^\_]+)_(?P<bypass>[\S|^\_]+)/$', views.model_select, name='model_select'),
    url(r'^model_(?P<id>\w+)', views.model, name='model'),
    url(r'^scoring_(?P<scorer>\w+)_(?P<target>\w+)_(?P<cutoff>\w+)/$', views.scoring, name='scoring'),
    url(r'^method/$', views.method, name='method'),
    url(r'^refinement_(?P<method>\w+)_(?P<refinement>\w+)_(?P<target>\w+)_(?P<cutoff>\w+)/$', views.refinement, name='refinement'),
    url(r'^about/$', views.about, name='about'),
    url(r'^refinement/$', views.refinement, name='refinement'),
    url(r'^noresults/$', views.noresults, name='noresults'),
    url(r'^refine_search_(?P<target>[\S|^\_]+)_(?P<method>[\S|^\_]+)_(?P<refinement>[\S|^\_]+)_(?P<i_rmsd_t>[\S|^\_]+)_(?P<l_rmsd_t>[\S|^\_]+)_(?P<r_rmsd_t>[\S|^\_]+)_(?P<fnat_t>[\S|^\_]+)_(?P<rank_str>[\S|^\_]+)_(?P<count>\w+)/$', views.refine_search, name='refine_search'),
)
