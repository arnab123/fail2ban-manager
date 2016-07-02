from django import forms

from .models import Filter
from .models import Action
from .models import DefaultJail
from .models import Jail

class FilterForm(forms.ModelForm):
	filter_name = forms.CharField(label='Name', max_length=30, widget=forms.TextInput(attrs={'class': "inputtext", 'type': "text"}))
	filter_desc = forms.CharField(label='Description', max_length=500, widget=forms.Textarea())
	filter_data = forms.CharField(label='Data', max_length=5000, widget=forms.Textarea())
	
	class Meta:
		model = Filter
		exclude = []
	def clean_filter_name(self):
		return self.cleaned_data.get('filter_name')
	def clean_filter_desc(self):
		return self.cleaned_data.get('filter_desc')
	def clean_filter_data(self):
		return self.cleaned_data.get('filter_data')


class ActionForm(forms.ModelForm):
	action_name = forms.CharField(label='Name', max_length=30, widget=forms.TextInput(attrs={'class': "inputtext", 'type': "text"}))
	action_desc = forms.CharField(label='Description', max_length=500, widget=forms.Textarea())
	action_data = forms.CharField(label='Data', max_length=5000, widget=forms.Textarea())
	
	class Meta:
		model = Action
		exclude = []
	def clean_action_name(self):
		return self.cleaned_data.get('action_name')
	def clean_action_desc(self):
		return self.cleaned_data.get('action_desc')
	def clean_action_data(self):
		return self.cleaned_data.get('action_data')


class FilterEditForm(forms.Form):
	filter_name = forms.CharField(label='Name', max_length=30, widget=forms.TextInput(attrs={'class': "inputtext", 'type': "text"}))
	filter_desc = forms.CharField(label='Description', max_length=500, widget=forms.Textarea())
	filter_data = forms.CharField(label='Data', max_length=5000, widget=forms.Textarea())
	
	def clean_filter_name(self):
		return self.cleaned_data.get('filter_name')
	def clean_filter_desc(self):
		return self.cleaned_data.get('filter_desc')
	def clean_filter_data(self):
		return self.cleaned_data.get('filter_data')

class ActionEditForm(forms.Form):
	action_name = forms.CharField(label='Name', max_length=30, widget=forms.TextInput(attrs={'class': "inputtext", 'type': "text"}))
	action_desc = forms.CharField(label='Description', max_length=500, widget=forms.Textarea())
	action_data = forms.CharField(label='Data', max_length=5000, widget=forms.Textarea())
	
	def clean_action_name(self):
		return self.cleaned_data.get('action_name')
	def clean_action_desc(self):
		return self.cleaned_data.get('action_desc')
	def clean_action_data(self):
		return self.cleaned_data.get('action_data')


class DefaultJailEditForm(forms.ModelForm):
	ignoreip = forms.CharField(max_length=500)
	bantime = forms.IntegerField()
	findtime = forms.IntegerField()
	maxretry = forms.IntegerField()
	backend = forms.ChoiceField(choices=DefaultJail.BACKEND_CHOICE)
	usedns = forms.ChoiceField(choices=DefaultJail.USEDNS_CHOICE)
	class Meta:
		model = DefaultJail
		exclude = []

class JailForm(forms.ModelForm):
	ignoreip = forms.CharField(max_length=500)
	bantime = forms.IntegerField()
	findtime = forms.IntegerField()
	maxretry = forms.IntegerField()
	backend = forms.ChoiceField(choices=Jail.BACKEND_CHOICE)
	usedns = forms.ChoiceField(choices=Jail.USEDNS_CHOICE)
	jail_name = forms.CharField(max_length=20)
	jail_desc = forms.CharField(max_length=500, widget=forms.Textarea())
	jail_data = forms.CharField(max_length=1000, widget=forms.Textarea())
	jail_actionvars = forms.CharField(max_length=200, widget=forms.Textarea())
	jail_filter = forms.ModelChoiceField(queryset=Filter.objects.all())
	jail_action = forms.ModelChoiceField(queryset=Action.objects.all())
	logpath = forms.CharField(max_length=300)
	enabled = forms.ChoiceField(choices=Jail.ENABLED_CHOICE)
	class Meta:
		model = Jail
		exclude = []

class JailEditForm(forms.Form):
	ignoreip = forms.CharField(max_length=500)
	bantime = forms.IntegerField()
	findtime = forms.IntegerField()
	maxretry = forms.IntegerField()
	backend = forms.ChoiceField(choices=Jail.BACKEND_CHOICE)
	usedns = forms.ChoiceField(choices=Jail.USEDNS_CHOICE)
	jail_name = forms.CharField(max_length=20)
	jail_desc = forms.CharField(max_length=500, widget=forms.Textarea())
	jail_data = forms.CharField(max_length=1000, widget=forms.Textarea())
	jail_actionvars = forms.CharField(max_length=200, widget=forms.Textarea())
	jail_filter = forms.ModelChoiceField(queryset=Filter.objects.all())
	jail_action = forms.ModelChoiceField(queryset=Action.objects.all())
	logpath = forms.CharField(max_length=300)
	enabled = forms.ChoiceField(choices=Jail.ENABLED_CHOICE)
