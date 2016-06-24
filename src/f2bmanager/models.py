from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Filter(models.Model):
	filter_name = models.CharField(max_length=20, unique=True)
	filter_desc = models.CharField(max_length=500, blank=True)
	filter_data = models.CharField(max_length=5000)
	created = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __unicode__(self):
		return self.name

class Action(models.Model):
	name = models.CharField(max_length=20)
	description = models.CharField(max_length=500, blank=True)
	created = models.DateTimeField(auto_now=False, auto_now_add=True);
	updated = models.DateTimeField(auto_now=True, auto_now_add=False);

	def __unicode__(self):
		return self.name


