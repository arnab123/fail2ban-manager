from django.shortcuts import render

from django.http import HttpResponseRedirect
from .forms import FilterForm

from django.db import IntegrityError


# Create your views here.


def get_manager(request):
	form = FilterForm(request.POST or None)
	context =  {
		'form': form,
	}
	if form.is_valid():
		print form
		form.save()
	return render(request, 'manager.html', context)


def home(request):
	return render(request,"home.html", {})

def add_filter(request):
	default_filter_data = '[INCLUDES]\n\n# Read common prefixes. \
	If any customizations available -- read them from\n# common.local\nbefore =\
	 common.conf\n\n\n[Definition]\n\nfailregex = \n\nignoreregex = '
	form = FilterForm(request.POST or None, initial={'filter_data': default_filter_data})
	context =  {
		'form': form,
		'name_error': '0',
	}

	if form.is_valid():
		instance = form.save(commit=False)	
		name_data = form.cleaned_data.get("filter_name")
		desc_data = form.cleaned_data.get("filter_desc")
		data_data = form.cleaned_data.get("filter_data")
		#print name_data
		#print desc_data
		#print data_data
		instance.filter_name = name_data
		instance.filter_desc = desc_data
		instance.filter_data = data_data
		instance.save()
		return HttpResponseRedirect('/saved/')
	# except IntegrityError as e:
	# 	print 'ERROR'
	# 	context['name_error'] = '1'
	return render(request,"add_filter.html", context)

def manager(request):
	return render(request,"manager.html", {})


	