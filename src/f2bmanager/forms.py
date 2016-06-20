from django import forms

from .models import Filter
from .models import Action

class FilterForm(forms.ModelForm):
	class Meta:
		model = Filter
		exclude = []

class ActionForm(forms.ModelForm):
	class Meta:
		model = Action
		exclude = []

class FilterDataForm(forms.Form):
	filter_data = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'size': '40'}))

