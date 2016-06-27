from django import forms

from .models import Filter
from .models import Action

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
