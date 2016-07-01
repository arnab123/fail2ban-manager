from django.shortcuts import render

from django.http import HttpResponseRedirect
from .forms import FilterForm
from .forms import ActionForm
from .forms import FilterEditForm
from .forms import ActionEditForm
from django.db import IntegrityError

from .models import Filter
from .models import Action

from django.utils.safestring import mark_safe
import os

# Create your views here.


def get_manager(request):
	# form = FilterForm(request.POST or None)
	# context =  {
	# 	'form': form,
	# }
	# if form.is_valid():
	# 	print form
	# 	form.save()
	form = FilterEditForm(request.POST or None)
	context =  {
		'form': form,
		'name_error': '0',
	}
	os.system('python f2bmanager/backend/change_name.py prev_name final_name')
	return render(request, 'edit_filter.html', context)


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
	if request.method == "POST":
		if form.is_valid():
			instance = form.save(commit=False)	
			name_data = form.cleaned_data.get("filter_name")
			desc_data = form.cleaned_data.get("filter_desc")
			data_data = form.cleaned_data.get("filter_data")
			#print name_data #print desc_data #print data_data
			instance.filter_name = name_data
			instance.filter_desc = desc_data
			instance.filter_data = data_data
			instance.save()
			return HttpResponseRedirect('/managefilters/')
		else:
			if Filter.objects.filter(filter_name=form.data['filter_name']).count() > 0:
				context['name_error']='1'
	# print Filter.objects.all()
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
	if request.method == "POST":
		if form.is_valid():
			instance = form.save(commit=False)	
			name_data = form.cleaned_data.get("action_name")
			desc_data = form.cleaned_data.get("action_desc")
			data_data = form.cleaned_data.get("action_data")
			#print name_data 	#print desc_data   #print data_data
			instance.action_name = name_data
			instance.action_desc = desc_data
			instance.action_data = data_data
			instance.save()
			return HttpResponseRedirect('/manageactions/')
		else:
			if Action.objects.filter(action_name=form.data['action_name']).count() > 0:
				context['name_error']='1'
	return render(request,"add_action.html", context)

filter_edit_name = ''
action_edit_name = ''

def edit_filter(request):
	init_name = ''
	init_data = ''
	init_desc = ''
	req = request.GET
	name = req.get('name')
	print name
	qset = Filter.objects.filter(filter_name=name)
	if qset.count() < 1:
		raise Exception('Filter entry with the given name doesn\'t exist')
	elif qset.count() > 1:
		raise Exception('More than one filters with the given name exists')
	for i in qset:
		init_name = i.filter_name
		init_data = i.filter_data
		init_desc = i.filter_desc
	form = FilterEditForm(request.POST or None, initial={'filter_name': init_name, \
		'filter_desc': init_desc, 'filter_data': init_data})
	context =  {
		'form': form,
		'name_error': '0',
	}
	if request.method == "POST":
		if form.is_valid():
			name_data = form.cleaned_data.get("filter_name")
			desc_data = form.cleaned_data.get("filter_desc")
			data_data = form.cleaned_data.get("filter_data")
			# print name_data			# print desc_data    # print data_data
			try:
				qset.update(filter_name=name_data, filter_desc=desc_data, filter_data=data_data)
				return HttpResponseRedirect('/managefilters/')
			except IntegrityError as e:
				context['name_error']='1'
		else:
			pass
	return render(request,"edit_filter.html", context)

def edit_action(request):
	init_name = ''
	init_data = ''
	init_desc = ''
	req = request.GET
	name = req.get('name')
	print name
	qset = Action.objects.filter(action_name=name)
	if qset.count() < 1:
		raise Exception('Action entry with the given name doesn\'t exist')
	elif qset.count() > 1:
		raise Exception('More than one actions with the given name exists')
	for i in qset:
		init_name = i.action_name
		init_data = i.action_data
		init_desc = i.action_desc
	form = ActionEditForm(request.POST or None, initial={'action_name': init_name, \
		'action_desc': init_desc, 'action_data': init_data})
	context =  {
		'form': form,
		'name_error': '0',
	}
	if request.method == "POST":
		if form.is_valid():
			name_data = form.cleaned_data.get("action_name")
			desc_data = form.cleaned_data.get("action_desc")
			data_data = form.cleaned_data.get("action_data")
			# print name_data			# print desc_data    # print data_data
			try:
				qset.update(action_name=name_data, action_desc=desc_data, action_data=data_data)
				return HttpResponseRedirect('/manageactions/')
			except IntegrityError as e:
				context['name_error']='1'
		else:
			pass
	return render(request,"edit_action.html", context)


def manage_filters(request):
	context =  {
		'tlist': Filter.objects.order_by('filter_name'),
	}
	return render(request, 'manage_filters.html', context)

def manage_actions(request):
	context =  {
		'tlist': Action.objects.order_by('action_name'),
	}
	return render(request, 'manage_actions.html', context)

def view_filter(request):
	name = request.GET.get('name')
	qset = Filter.objects.filter(filter_name=name)
	if qset.count() < 1:
		raise Exception('Filter entry with the given name doesn\'t exist')
	elif qset.count() > 1:
		raise Exception('More than one filters with the given name exists')
	data = ''
	for i in qset:
		data = i.filter_data
	context = {
		'name' : name,
		'data' : mark_safe(data),
	}
	return render(request, 'view.html', context)

def view_action(request):
	name = request.GET.get('name')
	qset = Action.objects.filter(action_name=name)
	if qset.count() < 1:
		raise Exception('Action entry with the given name doesn\'t exist')
	elif qset.count() > 1:
		raise Exception('More than one actions with the given name exists')
	data = ''
	for i in qset:
		data = i.action_data
	context = {
		'name' : name,
		'data' : mark_safe(data),
	}
	return render(request, 'view.html', context)

def delete_filter(request):
	name = request.GET.get('name')
	qset = Filter.objects.filter(filter_name=name)
	if qset.count() < 1:
		raise Exception('Filter entry with the given name doesn\'t exist')
	elif qset.count() > 1:
		raise Exception('More than one filters with the given name exists')
	qset.delete()
	print name
	return render(request, 'empty.html', {})

def delete_action(request):
	name = request.GET.get('name')
	qset = Action.objects.filter(action_name=name)
	if qset.count() < 1:
		raise Exception('Action entry with the given name doesn\'t exist')
	elif qset.count() > 1:
		raise Exception('More than one actions with the given name exists')
	qset.delete()
	print name
	return render(request, 'empty.html', {})

	