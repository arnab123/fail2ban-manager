from django import forms

from .models import DefaultJail
from .models import Jail
from .models import CustomFilter
from .models import CustomAction
from .models import Host
from .models import Membership

class DefaultJailEditForm(forms.ModelForm):
	ignoreip = forms.CharField(label='Ignore IP', max_length=500)
	bantime = forms.IntegerField(label='Bantime')
	findtime = forms.IntegerField(label='Findtime')
	maxretry = forms.IntegerField(label='Max Retries')
	# backend = forms.ChoiceField(label='Backend Type', choices=DefaultJail.BACKEND_CHOICE)
	# usedns = forms.ChoiceField(label='Use DNS', choices=DefaultJail.USEDNS_CHOICE)
	class Meta:
		model = DefaultJail
		exclude = []

class JailForm(forms.ModelForm):
	ignoreip = forms.CharField(label='Ignore IP', max_length=500)
	bantime = forms.IntegerField(label='Bantime')
	findtime = forms.IntegerField(label='Findtime')
	maxretry = forms.IntegerField(label='Max Retries')
	# backend = forms.ChoiceField(label='Backend Type', choices=Jail.BACKEND_CHOICE)
	# usedns = forms.ChoiceField(label='Use DNS', choices=Jail.USEDNS_CHOICE)
	jail_name = forms.CharField(label='Name', max_length=20)
	jail_desc = forms.CharField(label='Description', max_length=500, widget=forms.Textarea(), required=False)
	jail_data = forms.CharField(label='', max_length=1000, widget=forms.Textarea(), required=False)
#	jail_actionvars = forms.CharField(label='Jail Action Variables', max_length=200, widget=forms.Textarea())
	jail_filter = forms.ModelChoiceField(label='Filter', queryset=CustomFilter.objects.all())
	jail_action = forms.ModelChoiceField(label='Action', queryset=CustomAction.objects.all())
	logpath = forms.CharField(label='Log Path', max_length=300)
	enabled = forms.ChoiceField(label='Enable', choices=Jail.ENABLED_CHOICE)
	class Meta:
		model = Jail
		exclude = []

class JailEditForm(forms.Form):
	ignoreip = forms.CharField(label='Ignore IP',max_length=500)
	bantime = forms.IntegerField(label='Bantime')
	findtime = forms.IntegerField(label='Findtime')
	maxretry = forms.IntegerField(label='Max Retries')
	# backend = forms.ChoiceField(label='Backend Type', choices=Jail.BACKEND_CHOICE)
	# usedns = forms.ChoiceField(label='Use DNS', choices=Jail.USEDNS_CHOICE)
	jail_name = forms.CharField(label='Name', max_length=20)
	jail_desc = forms.CharField(label='Description', max_length=500, required=False, widget=forms.Textarea())
	jail_data = forms.CharField(label='', max_length=1000, widget=forms.Textarea(), required=False)
#	jail_actionvars = forms.CharField(label='Jail Action Variables', max_length=200, widget=forms.Textarea())
	jail_filter = forms.ModelChoiceField(label='Filter', queryset=CustomFilter.objects.all())
	jail_action = forms.ModelChoiceField(label='Action', queryset=CustomAction.objects.all())
	logpath = forms.CharField(label='Log Path', max_length=300)
	enabled = forms.ChoiceField(label='Enable', choices=Jail.ENABLED_CHOICE)

class CustomFilterForm(forms.ModelForm):
	filter_name = forms.CharField(label='Name', max_length=30, widget=forms.TextInput(attrs={'class': "inputtext", 'type': "text"}))
	filter_desc = forms.CharField(label='Description', max_length=500, widget=forms.Textarea())
	failregex = forms.CharField(label='Fail Regex', max_length=2000, widget=forms.Textarea())
	ignoreregex = forms.CharField(label='Ignore Regex', max_length=2000, widget=forms.Textarea(), required=False)
	filter_data = forms.CharField(label='Data', max_length=2000, widget=forms.Textarea(), required=False)
	
	class Meta:
		model = CustomFilter
		exclude = []
	def clean_filter_name(self):
		return self.cleaned_data.get('filter_name')
	def clean_filter_desc(self):
		return self.cleaned_data.get('filter_desc')
	def clean_failregex(self):
		a = self.cleaned_data.get('failregex')
		return a
	def clean_ignoreregex(self):
		a = self.cleaned_data.get('ignoreregex')
		return a
	def clean_filter_data(self):
		return self.cleaned_data.get('filter_data')


class CustomActionForm(forms.ModelForm):
	action_name = forms.CharField(label='Name', max_length=30, widget=forms.TextInput(attrs={'class': "inputtext", 'type': "text"}))
	action_desc = forms.CharField(label='Description', max_length=500, widget=forms.Textarea(), required=False)
	block_type = forms.ChoiceField(label='Block Using', choices=CustomAction.BLOCKTYPE_CHOICE)
	ip_chain = forms.CharField(label='New Chain Name', max_length=100, required=False)
	ip_block_type = forms.ChoiceField(label='Block Type', choices=CustomAction.IPBLOCKTYPE_CHOICE)
	ip_port = forms.CharField(label='Port (# or name)', max_length=30, required=False)
	ip_protocol = forms.ChoiceField(label='Protocol', choices=CustomAction.IPPROTOCOL_CHOICE)
	tcp_file = forms.CharField(label='', max_length=300, required=False)
	tcp_block_type = forms.ChoiceField(label='Block Type', choices=CustomAction.TCPBLOCKTYPE_CHOICE)
	action_data = forms.CharField(label='Data', max_length=2000, widget=forms.Textarea(), required=False)
	
	class Meta:
		model = CustomAction
		exclude = []
	def clean_action_name(self):
		return self.cleaned_data.get('action_name')
	def clean_action_desc(self):
		return self.cleaned_data.get('action_desc')
	def clean_block_type(self):
		return self.cleaned_data.get('block_type')
	def clean_ip_chain(self):
		return self.cleaned_data.get('ip_chain')
	def clean_ip_block_type(self):
		return self.cleaned_data.get('ip_block_type')
	def clean_ip_port(self):
		return self.cleaned_data.get('ip_port')
	def clean_ip_protocol(self):
		return self.cleaned_data.get('ip_protocol')
	def clean_tcp_file(self):
		return self.cleaned_data.get('tcp_file')
	def clean_tcp_block_type(self):
		return self.cleaned_data.get('tcp_block_type')
	def clean_action_data(self):
		return self.cleaned_data.get('action_data')

class CustomFilterEditForm(forms.Form):
	filter_name = forms.CharField(label='Name', max_length=30, widget=forms.TextInput(attrs={'class': "inputtext", 'type': "text"}))
	filter_desc = forms.CharField(label='Description', max_length=500, widget=forms.Textarea())
	failregex = forms.CharField(label='Fail Regex', max_length=2000, widget=forms.Textarea())
	ignoreregex = forms.CharField(label='Ignore Regex', max_length=2000, widget=forms.Textarea(), required=False)
	filter_data = forms.CharField(label='Data', max_length=2000, widget=forms.Textarea(), required=False)
	
	def clean_filter_name(self):
		return self.cleaned_data.get('filter_name')
	def clean_filter_desc(self):
		return self.cleaned_data.get('filter_desc')
	def clean_failregex(self):
		return self.cleaned_data.get('failregex')
	def clean_ignoreregex(self):
		return self.cleaned_data.get('ignoreregex')
	def clean_filter_data(self):
		return self.cleaned_data.get('filter_data')


class CustomActionEditForm(forms.Form):
	action_name = forms.CharField(label='Name', max_length=30, widget=forms.TextInput(attrs={'class': "inputtext", 'type': "text"}))
	action_desc = forms.CharField(label='Description', max_length=500, widget=forms.Textarea(), required=False)
	block_type = forms.ChoiceField(label='Block Using', choices=CustomAction.BLOCKTYPE_CHOICE)
	ip_chain = forms.CharField(label='New Chain Name', max_length=100, required=False)
	ip_block_type = forms.ChoiceField(label='Block Type', choices=CustomAction.IPBLOCKTYPE_CHOICE)
	ip_port = forms.CharField(label='Port (# or name)', max_length=30, required=False)
	ip_protocol = forms.ChoiceField(label='Protocol', choices=CustomAction.IPPROTOCOL_CHOICE)
	tcp_file = forms.CharField(label='', max_length=300, required=False)
	tcp_block_type = forms.ChoiceField(label='Block Type', choices=CustomAction.TCPBLOCKTYPE_CHOICE)
	action_data = forms.CharField(label='Data', max_length=2000, widget=forms.Textarea(), required=False)
	
	def clean_action_name(self):
		return self.cleaned_data.get('action_name')
	def clean_action_desc(self):
		return self.cleaned_data.get('action_desc')
	def clean_block_type(self):
		return self.cleaned_data.get('block_type')
	def clean_ip_chain(self):
		return self.cleaned_data.get('ip_chain')
	def clean_ip_block_type(self):
		return self.cleaned_data.get('ip_block_type')
	def clean_tcp_file(self):
		return self.cleaned_data.get('tcp_file')
	def clean_tcp_block_type(self):
		return self.cleaned_data.get('tcp_block_type')
	def clean_action_data(self):
		return self.cleaned_data.get('action_data')

class HostForm(forms.ModelForm):
	host_name = forms.CharField(label='Name', max_length=200)
	ip = forms.CharField(label='IP', max_length=30)
	jail = forms.ModelMultipleChoiceField(label='Jails', queryset=Jail.objects.all())
	days = forms.IntegerField(label='Fetch last n days of log')
	class Meta:
		model = Host
		exclude = ['log', 'updated']

class HostEditForm(forms.Form):
	host_name = forms.CharField(label='Name', max_length=200)
	ip = forms.CharField(label='IP', max_length=30)
	jail = forms.ModelMultipleChoiceField(label='Jails', queryset=Jail.objects.all())
	days = forms.IntegerField(label='Fetch last n days of log')

class MultiAddForm(forms.Form):
	host = forms.ModelMultipleChoiceField(label='to the following hosts', queryset=Host.objects.all())
	jail = forms.ModelMultipleChoiceField(label='Add these jails', queryset=Jail.objects.all())

class LoginForm(forms.Form):
	username = forms.CharField(max_length=40,\
		widget=forms.TextInput(attrs={'class':"zocial-dribbble", 'type':"text", 'placeholder':"Username"}))
	password = forms.CharField(max_length=64,\
		widget=forms.PasswordInput(attrs={ 'type':"password", 'placeholder':"Password"}))
	