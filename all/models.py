# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Method(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30L)
    capri5_performance = models.IntegerField()
    description = models.CharField(max_length=100L)
    class Meta:
        db_table = 'method'

class Model(models.Model):
    id = models.IntegerField(primary_key=True)
    number = models.IntegerField()
    r_rmsd = models.FloatField()
    l_rmsd = models.FloatField()
    i_rmsd = models.FloatField()
    i_l_rmsd = models.FloatField()
    fnat = models.FloatField()
    no_clashes = models.IntegerField()
    capri_valid = models.IntegerField()
    asa_c = models.FloatField()
    asa_rl = models.FloatField()
    capri_ev = models.IntegerField()
    target = models.ForeignKey('Target')
    method = models.ForeignKey(Method)
    refinement = models.ForeignKey('Refinement')
    class Meta:
        db_table = 'model'

class ModelTemp(models.Model):
    number = models.IntegerField()
    r_rmsd = models.FloatField()
    l_rmsd = models.FloatField()
    i_rmsd = models.FloatField()
    i_l_rmsd = models.FloatField()
    fnat = models.FloatField()
    asa_c = models.FloatField()
    asa_rl = models.FloatField()
    no_clashes = models.IntegerField()
    capri_valid = models.IntegerField()
    capri_ev = models.IntegerField(null=True, blank=True)
    target = models.CharField(max_length=30L)
    method = models.CharField(max_length=30L)
    refinement = models.CharField(max_length=30L)
    id = models.IntegerField(primary_key=True)
    class Meta:
        db_table = 'model_temp'

class Refinement(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30L)
    description = models.CharField(max_length=100L)
    class Meta:
        db_table = 'refinement'

class Score(models.Model):
    id = models.IntegerField(primary_key=True)
    model = models.ForeignKey(Model)
    scoring_function = models.ForeignKey('ScoringFunction')
    score = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = 'score'

class ScoreTemp(models.Model):
    score = models.FloatField(null=True, blank=True)
    number = models.IntegerField()
    target = models.CharField(max_length=30L)
    method = models.CharField(max_length=30L)
    refinement = models.CharField(max_length=30L)
    scoring_function = models.CharField(max_length=30L)
    id = models.IntegerField(primary_key=True)
    class Meta:
        db_table = 'score_temp'

class ScoringFunction(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20L)
    description = models.CharField(max_length=200L)
    class Meta:
        db_table = 'scoring_function'

class Target(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50L)
    difficulty = models.CharField(max_length=20L)
    complex = models.CharField(max_length=4L)
    category = models.CharField(max_length=50L)
    r_rmsd = models.FloatField()
    l_rmsd = models.FloatField()
    i_rmsd = models.FloatField()
    i_l_rmsd = models.FloatField()
    asa_c_b = models.FloatField()
    asa_rl_b = models.FloatField()
    asa_c_u = models.FloatField()
    asa_rl_u = models.FloatField()
    receptor = models.CharField(max_length=4L)
    receptor_description = models.CharField(max_length=100L)
    receptor_bound_chain = models.CharField(max_length=10L)
    receptor_unbound_chain = models.CharField(max_length=10L)
    ligand = models.CharField(max_length=4L)
    ligand_bound_chain = models.CharField(max_length=10L)
    ligand_unbound_chain = models.CharField(max_length=10L)
    ligand_description = models.CharField(max_length=100L)
    source = models.CharField(max_length=100L)
    class Meta:
        db_table = 'target'

