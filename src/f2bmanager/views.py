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
    if request.method == 'POST':
        form = FilterDataForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    else:
        form = FilterDataForm()

    return render(request, 'manager.html', {'form': form})


def home(request):
	return render(request,"home.html", {})

def manager(request):
	return render(request,"manager.html", {})