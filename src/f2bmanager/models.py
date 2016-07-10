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
		return self.filter_name

class Action(models.Model):
	action_name = models.CharField(max_length=20, unique=True)
	action_desc = models.CharField(max_length=500, blank=True)
	action_data = models.CharField(max_length=5000)
	created = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __unicode__(self):
		return self.action_name

class DefaultJail(models.Model):
	BACKEND_CHOICE = (
		('auto', 'Auto'),
		('pyinotify', 'Pyinotify'),
		('gamin', 'Gamin'),
		('polling', 'Polling'),
    )
	USEDNS_CHOICE = (
		('warn', 'Warn'),
		('yes', 'Yes'),
		('no', 'No'),
    )
	ignoreip = models.CharField(max_length=500, blank=True, default='127.0.0.1/8')
	bantime = models.IntegerField(default=600)
	findtime = models.IntegerField(default=600)
	maxretry = models.IntegerField(default=3)
	backend = models.CharField(max_length=15, choices=BACKEND_CHOICE, default='auto')
	usedns = models.CharField(max_length=5, choices=USEDNS_CHOICE, default='warn')

	def __unicode__(self):
		return self.name

class Jail(models.Model):
	BACKEND_CHOICE = (
		('auto', 'Auto'),
		('pyinotify', 'Pyinotify'),
		('gamin', 'Gamin'),
		('polling', 'Polling'),
    )
	USEDNS_CHOICE = (
		('warn', 'Warn'),
		('yes', 'Yes'),
		('no', 'No'),
    )
	ignoreip = models.CharField(max_length=500, blank=True, default='127.0.0.1/8')
	bantime = models.IntegerField(default=600)
	findtime = models.IntegerField(default=600)
	maxretry = models.IntegerField(default=3)
	backend = models.CharField(max_length=15, choices=BACKEND_CHOICE, default='auto')
	usedns = models.CharField(max_length=5, choices=USEDNS_CHOICE, default='warn')
	
	ENABLED_CHOICE = (
		('true', 'True'),
		('false', 'False'),
	)
	jail_name = models.CharField(max_length=20, unique=True)
	jail_desc = models.CharField(max_length=500, blank=True)
	jail_data = models.CharField(max_length=1000, blank=True)
	jail_actionvars = models.CharField(max_length=200, blank=True)
	jail_filter = models.ForeignKey(Filter, blank=True)
	jail_action = models.ForeignKey(Action, blank=True)
	logpath = models.CharField(max_length=300)
	enabled = models.CharField(max_length=6, choices=ENABLED_CHOICE, default='true')

class CustomFilter(models.Model):
	filter_name = models.CharField(max_length=20, unique=True)
	filter_desc = models.CharField(max_length=500, null=True, blank=True)
	failregex = models.CharField(max_length=3000)
	ignoreregex = models.CharField(max_length=3000, null=True, blank=True)
	filter_data = models.CharField(max_length=2000,  null=True, blank=True)
	created = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __unicode__(self):
		return self.filter_name

class CustomAction(models.Model):
	action_name = models.CharField(max_length=20, unique=True)
	action_desc = models.CharField(max_length=500, null=True, blank=True)
	BLOCKTYPE_CHOICE = (
		('iptables', 'Iptables'),
		('tcp-wrapper', 'TCP-Wrapper'),
	)
	block_type = models.CharField(max_length=40, choices=BLOCKTYPE_CHOICE, default='iptables')
	ip_chain = models.CharField(max_length=20, null=True, blank=True)
	IPBLOCKTYPE_CHOICE = (
		('drop', 'Drop'),
		('reject', 'Reject with ICMP Message'),
	)
	ip_block_type = models.CharField(max_length=40, choices=IPBLOCKTYPE_CHOICE, default='drop', null=True, blank=True)
	tcp_file = models.CharField(max_length=80, null=True, blank=True)
	TCPBLOCKTYPE_CHOICE = (
		('ALL', 'ALL'),
		('SSH', 'SSH'),
	)
	tcp_block_type = models.CharField(max_length=20, choices=TCPBLOCKTYPE_CHOICE, default='ALL', null=True, blank=True)
	action_data = models.CharField(max_length=2000, null=True, blank=True)
	created = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __unicode__(self):
		return self.action_name


