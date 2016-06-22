from django.shortcuts import render

from django.http import HttpResponseRedirect

'''
from django import forms
class FilterDataForm(forms.Form):
	filter_data = forms.CharField(label='Filter Data', max_length=100)
'''
from .forms import FilterDataForm

# Create your views here.


def get_manager(request):

    form = FilterDataForm(request.POST or None)
    context =  {
    	'form': form
    }
    if form.is_valid():
        filter_data = form.cleaned_data.get("filter_data")

        return HttpResponseRedirect('/thanks/')

    return render(request, 'manager.html', context)


def home(request):
	return render(request,"home.html", {})

def add_filter(request):
	return render(request,"add_filter.html", {})

def manager(request):
	return render(request,"manager.html", {})