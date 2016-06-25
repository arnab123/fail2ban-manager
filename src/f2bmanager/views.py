from django.shortcuts import render

from django.http import HttpResponseRedirect
from .forms import FilterForm
from .forms import ActionForm
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

def add_action(request):
	default_action_data = '[INCLUDES]\n\nbefore = \n\n[Definition]\n\n# Option:  actions\
tart\n# Notes.:  command executed once at the start of Fail2Ban.\n# Values:  CMD\nactionst\
art = \n\n\n# Option:  actionstop\n# Notes.:  command executed once at the end of Fai\
l2Ban\n# Values:  CMD\nactionstop = \n\n\n# Option:  actioncheck\n# Notes.:  command exec\
uted once before each actionban command\n# Values:  CMD\nactioncheck = \n\n\n# Option:  actio\
nban\n# Notes.:  command executed when banning. Take care that the\n#          command is e\
xecuted with Fail2Ban user rights.\n# Values:  CMD\nactionban = \n\n\n# Option:  actionu\
nban\n# Notes.:  command executed when unbanning. Take care that the\n#          command is\
 executed with Fail2Ban user rights.\n# Values:  CMD\nactionunban = \n\n\n[Init]\n\n\n\n'
	form = ActionForm(request.POST or None, initial={'action_data': default_action_data})
	context =  {
		'form': form,
		'name_error': '0',
	}

	if form.is_valid():
		instance = form.save(commit=False)	
		name_data = form.cleaned_data.get("action_name")
		desc_data = form.cleaned_data.get("action_desc")
		data_data = form.cleaned_data.get("action_data")
		#print name_data
		#print desc_data
		#print data_data
		instance.action_name = name_data
		instance.action_desc = desc_data
		instance.action_data = data_data
		instance.save()
		return HttpResponseRedirect('/saved/')
	# except IntegrityError as e:
	# 	print 'ERROR'
	# 	context['name_error'] = '1'
	return render(request,"add_action.html", context)

def manager(request):
	return render(request,"manager.html", {})


	