from django.shortcuts import render

from django.http import HttpResponseRedirect
from .forms import FilterForm
from .forms import ActionForm
from .forms import FilterEditForm
from .forms import ActionEditForm
from .forms import DefaultJailEditForm
from .forms import JailForm
from .forms import JailEditForm
from django.db import IntegrityError

from .models import Filter
from .models import Action
from .models import DefaultJail
from .models import Jail

from django.utils.safestring import mark_safe

# Create your views here.


import os

# Create your views here.
def fail_start():
	os.system('sudo fail2ban-client start')

def fail_restart():
	os.system('sudo fail2ban-client reload')	

def make_file(location,name,data):
	os.system('python f2bmanager/backend/make_file.py ' + location + ' ' + name + ' ' + data)

def replace_jail(jail,para,value):
	os.system('python f2bmanager/backend/change_jail_para.py ' + jail + ' ' + para + ' ' + value)

def edit_form(prev_name,new_name):
	os.system('python f2bmanager/backend/change_name.py ' + prev_name + ' ' +new_name)

def get_manager(request):

	# edit_form('hell','finally')
	# replace_jail('ssh','enabled','false')
	make_file('action.d','abhi','Yooo')
	return render(request, 'empty.html', {})

def onFilterEdit(name):
	obj = Filter.objects.get(filter_name=name)
	make_file('filter.d', obj.filter_name, obj.filter_data)
	#fail_restart()

def onActionEdit(name):
	obj = Action.objects.get(action_name=name)
	make_file('action.d', obj.action_name, obj.action_data)
	#fail_restart()



def makeJailData(name):
	i = Jail.objects.get(jail_name=name)
	data = ''
	data += '['+i.jail_name+']\n\n'
	data += 'enabled = '+i.enabled +'\n'
	data += 'ignoreip = '+i.ignoreip +'\n'
	data += 'bantime = '+str(i.bantime) +'\n'
	data += 'findtime = '+str(i.findtime) +'\n'
	data += 'maxretry = '+str(i.maxretry) +'\n'
	data += 'backend = '+i.backend +'\n'
	data += 'usedns = '+i.usedns+'\n'
	data += 'filter = '+str(i.jail_filter)+'\n'
	data += 'action = '+str(i.jail_action) +'['+i.jail_actionvars+']\n'
	data += 'logpath = '+i.logpath +'\n'
	data += i.jail_data + '\n\n'
	return data

def onDeploy():
	print 'Deploy Called'
	qset = Jail.objects.all()
	temp = ''
	for i in qset:
		temp += makeJailData(i.jail_name)
		onFilterEdit(str(i.jail_filter))
		onActionEdit(str(i.jail_action))
	os.system('echo \"' + temp + '\" > /etc/fail2ban/jail.local')
	fail_restart()



def home(request):
	onDeploy()
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

def edit_defaultjail(request):
	qset = DefaultJail.objects.all()
	init_ignoreip = ''
	init_bantime = ''
	init_findtime = ''
	init_maxretry = ''
	init_backend = ''
	init_usedns = ''
	for i in qset:
		init_ignoreip = i.ignoreip
		init_bantime = i.bantime
		init_findtime = i.findtime
		init_maxretry = i.maxretry
		init_backend = i.backend
		init_usedns = i.usedns
	form = DefaultJailEditForm(request.POST or None, initial={'ignoreip': init_ignoreip, \
		'bantime':init_bantime,\
		'findtime':init_findtime,\
		'maxretry':init_maxretry,\
		'backend':init_backend,\
		'usedns':init_usedns})
	context =  {
		'form': form,
	}
	if request.method == "POST":
		#print form
		if form.is_valid():
			qset.delete()
			form.save()
			return HttpResponseRedirect('/managejails/')
		else:
			pass
	return render(request,"edit_defaultjail.html", context)

def add_jail(request):
	qset = DefaultJail.objects.all()
	init_ignoreip = ''
	init_bantime = ''
	init_findtime = ''
	init_maxretry = ''
	init_backend = ''
	init_usedns = ''
	for i in qset:
		init_ignoreip = i.ignoreip
		init_bantime = i.bantime
		init_findtime = i.findtime
		init_maxretry = i.maxretry
		init_backend = i.backend
		init_usedns = i.usedns
	form = JailForm(request.POST or None, initial={'ignoreip': init_ignoreip, \
		'bantime':init_bantime,\
		'findtime':init_findtime,\
		'maxretry':init_maxretry,\
		'backend':init_backend,\
		'usedns':init_usedns})
	context =  {
		'form': form,
	}
	if request.method == "POST":
		#print form
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/managejails/')
		else:
			pass
	return render(request,"add_jail.html", context)

def edit_jail(request):
	name = request.GET.get('name')
	qset = Jail.objects.filter(jail_name=name)
	if qset.count() < 1:
		raise Exception('Jail entry with the given name doesn\'t exist')
	elif qset.count() > 1:
		raise Exception('More than one jails with the given name exists')
	init_ignoreip = ''
	init_bantime = ''
	init_findtime = ''
	init_maxretry = ''
	init_backend = ''
	init_usedns = ''
	init_jail_name = ''
	init_jail_desc = ''
	init_jail_data = ''
	init_jail_actionvars = ''
	init_jail_filter = ''
	init_jail_action = ''
	init_logpath = ''
	init_enabled = ''

	for i in qset:
		init_ignoreip = i.ignoreip
		init_bantime = i.bantime
		init_findtime = i.findtime
		init_maxretry = i.maxretry
		init_backend = i.backend
		init_usedns = i.usedns
		init_jail_name = i.jail_name
		init_jail_desc = i.jail_desc
		init_jail_data = i.jail_data
		init_jail_actionvars = i.jail_actionvars
		init_jail_filter = i.jail_filter
		init_jail_action = i.jail_action
		init_logpath = i.logpath
		init_enabled = i.enabled
	form = JailEditForm(request.POST or None, initial={'ignoreip': init_ignoreip, \
		'bantime':init_bantime,\
		'findtime':init_findtime,\
		'maxretry':init_maxretry,\
		'backend':init_backend,\
		'usedns':init_usedns,\
		'jail_name':init_jail_name,\
		'jail_desc':init_jail_desc,\
		'jail_data':init_jail_data,\
		'jail_actionvars':init_jail_actionvars,\
		'jail_filter':init_jail_filter,\
		'jail_action':init_jail_action,\
		'logpath':init_logpath,\
		'enabled':init_enabled,\
		})
	context =  {
		'form': form,
	}
	if request.method == "POST":
		#print form
		if form.is_valid():
			qset.update(\
				ignoreip = form.cleaned_data.get("ignoreip"),\
				bantime = form.cleaned_data.get("bantime"),\
				findtime = form.cleaned_data.get("findtime"),\
				maxretry = form.cleaned_data.get("maxretry"),\
				backend = form.cleaned_data.get("backend"),\
				usedns = form.cleaned_data.get("usedns"),\
				jail_name = form.cleaned_data.get("jail_name"),\
				jail_desc = form.cleaned_data.get("jail_desc"),\
				jail_data = form.cleaned_data.get("jail_data"),\
				jail_actionvars = form.cleaned_data.get("jail_actionvars"),\
				jail_filter = form.cleaned_data.get("jail_filter"),\
				jail_action = form.cleaned_data.get("jail_action"),\
				logpath = form.cleaned_data.get("logpath"),\
				enabled = form.cleaned_data.get("enabled")\
			)
			return HttpResponseRedirect('/managejails/')
		else:
			pass
	return render(request,"edit_jail.html", context)

def manage_jails(request):
	context =  {
		'tlist': Jail.objects.order_by('jail_name'),
	}
	return render(request, 'manage_jails.html', context)

def view_jail(request):
	name = request.GET.get('name')
	qset = Jail.objects.filter(jail_name=name)
	if qset.count() < 1:
		raise Exception('Jail entry with the given name doesn\'t exist')
	elif qset.count() > 1:
		raise Exception('More than one jails with the given name exists')
	data = ''
	for i in qset:
		data += '['+i.jail_name+']<br><br>'
		data += 'enabled = '+i.enabled +'<br>'
		data += 'ignoreip = '+i.ignoreip +'<br>'
		data += 'bantime = '+str(i.bantime) +'<br>'
		data += 'findtime = '+str(i.findtime) +'<br>'
		data += 'maxretry = '+str(i.maxretry) +'<br>'
		data += 'backend = '+i.backend +'<br>'
		data += 'usedns = '+i.usedns+'<br>'
		data += 'filter = '+str(i.jail_filter)+'<br>'
		data += 'action = '+str(i.jail_action) +'['+i.jail_actionvars+']<br>'
		data += 'logpath = '+i.logpath +'<br>'
		data += i.jail_data
	context = {
		'name' : name,
		'data' : mark_safe(data),
	}
	return render(request, 'view.html', context)

def delete_jail(request):
	name = request.GET.get('name')
	qset = Jail.objects.filter(jail_name=name)
	if qset.count() < 1:
		raise Exception('Jail entry with the given name doesn\'t exist')
	elif qset.count() > 1:
		raise Exception('More than one jails with the given name exists')
	qset.delete()
	return render(request, 'empty.html', {})