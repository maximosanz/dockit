from django.conf.urls import patterns, url

from all import views

urlpatterns = patterns('',
    url(r'^$', views.search, name='search'),
    url(r'^summary_(?P<target>\w+)/$', views.summary, name='summary'),
    url(r'^target/$', views.target, name='target'),
    url(r'^target/(?P<name>\w+)/$', views.target_info, name='target_info'),
    url(r'^model_select_(?P<target>\w+)_(?P<method>\w+)/$', views.model_select, name='model_select'),
    url(r'^model_(?P<id>\w+)', views.model, name='model'),
    url(r'^scoring_(?P<scorer>\w+)_(?P<target>\w+)/$', views.scoring, name='scoring'),
    url(r'^method/$', views.method, name='method'),
    url(r'^refinement/$', views.refinement, name='refinement'),
    url(r'^model_select_(?P<target>[\S|^\_]+)_(?P<method>[\S|^\_]+)_(?P<refinement>[\S|^\_]+)_(?P<i_rmsd_threshold>[\S|^\_]+)_(?P<l_rmsd_threshold>[\S|^\_]+)_(?P<r_rmsd_threshold>[\S|^\_]+)_(?P<fnat_threshold>[\S|^\_]+)/$', views.model_select, name='model_select'),
)
