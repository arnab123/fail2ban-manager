from __future__ import unicode_literals

from django.db import models

# Create your models here.


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
		('DROP', 'Drop'),
		('REJECT --reject-with icmp-port-unreachable', 'Reject with ICMP Message'),
	)
	ip_block_type = models.CharField(max_length=100, choices=IPBLOCKTYPE_CHOICE, default='drop', null=True, blank=True)
	ip_port = models.CharField(max_length=30, default='ssh', null=True, blank=True)
	IPPROTOCOL_CHOICE = (
		('tcp', 'TCP'),
		('udp', 'UDP'),
		('icmp', 'ICMP'),
		('all', 'ALL'),
	)
	ip_protocol = models.CharField(max_length=10, choices=IPPROTOCOL_CHOICE, default='tcp', null=True, blank=True)
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
	ignoreip = models.CharField(max_length=500, blank=True, default='127.0.0.1/8', null=True)
	bantime = models.IntegerField(default=600)
	findtime = models.IntegerField(default=600)
	maxretry = models.IntegerField(default=3)
	# backend = models.CharField(max_length=15, choices=BACKEND_CHOICE, default='auto')
	# usedns = models.CharField(max_length=5, choices=USEDNS_CHOICE, default='warn')

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
	ignoreip = models.CharField(max_length=500, blank=True, default='127.0.0.1/8', null=True)
	bantime = models.IntegerField(default=600)
	findtime = models.IntegerField(default=600)
	maxretry = models.IntegerField(default=3)
	# backend = models.CharField(max_length=15, choices=BACKEND_CHOICE, default='auto')
	# usedns = models.CharField(max_length=5, choices=USEDNS_CHOICE, default='warn')
	
	ENABLED_CHOICE = (
		('true', 'True'),
		('false', 'False'),
	)
	jail_name = models.CharField(max_length=20, unique=True)
	jail_desc = models.CharField(max_length=500, blank=True)
	jail_data = models.CharField(max_length=1000, blank=True)
#	jail_actionvars = models.CharField(max_length=200, blank=True)
	jail_filter = models.ForeignKey(CustomFilter, blank=True)
	jail_action = models.ForeignKey(CustomAction, blank=True)
	logpath = models.CharField(max_length=300)
	enabled = models.CharField(max_length=6, choices=ENABLED_CHOICE, default='true')

	def __unicode__(self):
		return self.jail_name


class Host(models.Model):
	host_name = models.CharField(max_length=200, unique=True)
	ip = models.CharField(max_length=30, unique=True)
	jail = models.ManyToManyField(Jail, through='Membership')
	log = models.TextField(null=True)
	updated = models.DateTimeField(null=True)
	days = models.IntegerField(default=5)

	def __unicode__(self):
		return self.host_name


class Membership(models.Model):
	host = models.ForeignKey(Host, on_delete=models.CASCADE)
	jail = models.ForeignKey(Jail, on_delete=models.CASCADE)
	addedon = models.DateTimeField(auto_now=False, auto_now_add=True)

	class Meta:
		unique_together = ('host', 'jail',)




