from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .forms import CustomFilterForm
from .forms import CustomActionForm
from .forms import CustomFilterEditForm
from .forms import CustomActionEditForm
from .forms import DefaultJailEditForm
from .forms import JailForm
from .forms import JailEditForm
from .forms import HostForm
from .forms import HostEditForm
from .forms import MultiAddForm
from .forms import LoginForm

from .models import CustomFilter
from .models import CustomAction
from .models import DefaultJail
from .models import Jail
from .models import Host
from .models import Membership

from .strings import Res

import datetime
import os

# Create your views here.
def fail_start():
	os.system('sudo fail2ban-client start')

def fail_restart():
	os.system('sudo fail2ban-client reload')	

def remote_fail_restart(ip):
	#os.system('sshpass -p "" ssh @ "fail2ban-client start"')
	#os.system('sudo fail2ban-client reload')
	pass

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



def makeJailData(i):
#	i = Jail.objects.get(jail_name=name)
	data = ''
	data += '['+i.jail_name+']\n\n'
	data += 'enabled = '+i.enabled +'\n'
	data += 'ignoreip = '+i.ignoreip +'\n'
	data += 'bantime = '+str(i.bantime) +'\n'
	data += 'findtime = '+str(i.findtime) +'\n'
	data += 'maxretry = '+str(i.maxretry) +'\n'
	# data += 'backend = '+i.backend +'\n'
	# data += 'usedns = '+i.usedns+'\n'
	data += 'filter = '+str(i.jail_filter)+'\n'
	data += 'action = '+str(i.jail_action)+'\n'
	data += 'logpath = '+i.logpath +'\n'
	data += i.jail_data + '\n\n'
	return data

def onDeploy():
	for i in Jail.objects.all():
		addJailLocal(i)
	os.system('./f2bmanager/suids/writefilter')
	os.system('./f2bmanager/suids/writeaction')
	os.system('./f2bmanager/suids/writejail')
	os.system('./f2bmanager/suids/failreload')

def addFilterLocal(filt):
	filt_data = Res.filter_sshd.replace("<<failregex>>", filt.failregex)
	filt_data = filt_data.replace("<<ignoreregex>>", filt.ignoreregex)
	filt_name = filt.filter_name
	file_name = filt_name+'.conf'
	print filt_data
	f = open('/tmp/fail2ban/filter.d/'+file_name, 'w')
	f.write(filt_data)
	f.close()
	#os.system('sshpass -p "" scp -r ~/django/proj/src/f2bmanager/'+file_name+' @:/etc/fail2ban/filter.d/')
	#add

def addActionLocal(act):
	act_data = ''
	act_name = act.action_name
	if act.block_type == "iptables":
		act_data = Res.action_iptables.replace("<<name>>",act.ip_chain)
		act_data = act_data.replace("<<port>>",act.ip_port)
		act_data = act_data.replace("<<protocol>>",act.ip_protocol)
		act_data = act_data.replace("<<blocktype>>",act.ip_block_type)
	elif act.block_type == "tcp-wrapper":
		act_data = Res.action_hostsdeny.replace("<<file>>",act.tcp_file)
		act_data = act_data.replace("<<blocktype>>",act.tcp_block_type)
	file_name = act_name+'.conf'
	print act_data
	f = open('/tmp/fail2ban/action.d/'+file_name, 'w')
	f.write(act_data)
	f.close()
	#os.system('sshpass -p "" scp -r ~/django/proj/src/f2bmanager/'+file_name+' @:/etc/fail2ban/action.d/')
	

def addJailLocal(jail):
	addFilterLocal(jail.jail_filter)
	addActionLocal(jail.jail_action)
	jail_data = makeJailData(jail)
	print "addedjail "+jail.jail_name
	file_name = jail.jail_name + '.conf'
	f = open('/tmp/fail2ban/jail.d/'+file_name, 'w')
	f.write(jail_data)
	f.close()
	# os.system('sshpass -p "" scp -r ~/django/proj/src/f2bmanager/temp @:/etc/fail2ban/')
	# os.system('sshpass -p "" ssh @ "cat /etc/fail2ban/temp >> /etc/fail2ban/jail.local"')


def addFilterRemote(ip, filt):
	filt_data = Res.filter_sshd.replace("<<failregex>>", filt.failregex)
	filt_data = filt_data.replace("<<ignoreregex>>", filt.ignoreregex)
	filt_name = filt.filter_name
	file_name = filt_name+'.conf'
	print filt_data
	f = open('~/django/proj/src/f2bmanager/'+file_name, 'w')
	f.write(filt_data)
	f.close()
	#os.system('sshpass -p "" scp -r ~/django/proj/src/f2bmanager/'+file_name+' @:/etc/fail2ban/filter.d/')
	#add

def delFilterRemote(ip, filt):
	filt_name = filt.filter_name
	#add

def addActionRemote(ip, act):
	act_data = ''
	act_name = act.action_name
	if act.block_type == "iptables":
		act_data = Res.action_iptables.replace("<<name>>",act.ip_chain)
		act_data = act_data.replace("<<port>>",act.ip_port)
		act_data = act_data.replace("<<protocol>>",act.ip_port)
		act_data = act_data.replace("<<blocktype>>",act.ip_block_type)
	elif act.block_type == "tcp-wrapper":
		act_data = Res.action_hostsdeny.replace("<<file>>",act.tcp_file)
		act_data = act_data.replace("<<blocktype>>",act.tcp_block_type)
	file_name = act_name+'.conf'
	print act_data
	f = open('~/django/proj/src/f2bmanager/'+file_name, 'w')
	f.write(act_data)
	f.close()
	#os.system('sshpass -p "" scp -r ~/django/proj/src/f2bmanager/'+file_name+' @:/etc/fail2ban/action.d/')
	

def delActionRemote(ip, act):
	act_name = act.action_name


def addJailRemote(ip, jail):
	addFilterRemote(ip, jail.jail_filter)
	addActionRemote(ip, jail.jail_action)
	jail_data = makeJailData(jail)
	print "addedjail "+jail.jail_name
	f = open('~/django/proj/src/f2bmanager/temp', 'w')
	f.write(jail_data)
	f.close()
	# os.system('sshpass -p "" scp -r ~/django/proj/src/f2bmanager/temp @:/etc/fail2ban/')
	# os.system('sshpass -p "" ssh @ "cat /etc/fail2ban/temp >> /etc/fail2ban/jail.local"')

def delJailRemote(ip, jail):
	delFilterRemote(ip, jail.jail_filter)
	delActionRemote(ip, jail.jail_action)
	jail_name = jail.jail_name
	print "deleted jail" + jail_name


def home(request):
	form = LoginForm(request.POST or None)
	context ={
		'form' : form,
		'loginerror' : '0',
	}
	if request.method == "POST":
		if form.is_valid():
			# uname = form.cleaned_data.get('username')
			# passwd = form.cleaned_data.get('password')
			logout(request)
			uname = request.POST['username']
			passwd = request.POST['password']
			user = authenticate(username=uname, password=passwd)
			if user is not None:
				if user.is_active:
					print("User is valid, active and authenticated")
					login(request, user)
					return HttpResponseRedirect('/managejails/')
				else:
					print("The password is valid, but the account has been disabled!")
			else:
				print("The username and password were incorrect.")
				context['loginerror'] = '1'
				return render(request,"home.html", context)
		else:
			context['loginerror'] = '1'
			return render(request,"home.html", context)
	if request.user.is_authenticated():
		pass
	return render(request,"home.html", context)

def edit_defaultjail(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	qset = DefaultJail.objects.all()
	init_ignoreip = ''
	init_bantime = ''
	init_findtime = ''
	init_maxretry = ''
	# init_backend = ''
	# init_usedns = ''
	for i in qset:
		init_ignoreip = i.ignoreip
		init_bantime = i.bantime
		init_findtime = i.findtime
		init_maxretry = i.maxretry
		# init_backend = i.backend
		# init_usedns = i.usedns
	form = DefaultJailEditForm(request.POST or None, initial={'ignoreip': init_ignoreip, \
		'bantime':init_bantime,\
		'findtime':init_findtime,\
		'maxretry':init_maxretry})
		# 'backend':init_backend,\
		# 'usedns':init_usedns})
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
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	qset = DefaultJail.objects.all()
	init_ignoreip = ''
	init_bantime = ''
	init_findtime = ''
	init_maxretry = ''
	# init_backend = ''
	# init_usedns = ''
	for i in qset:
		init_ignoreip = i.ignoreip
		init_bantime = i.bantime
		init_findtime = i.findtime
		init_maxretry = i.maxretry
		# init_backend = i.backend
		# init_usedns = i.usedns
	form = JailForm(request.POST or None, initial={'ignoreip': init_ignoreip, \
		'bantime':init_bantime,\
		'findtime':init_findtime,\
		'maxretry':init_maxretry})
		# 'backend':init_backend,\
		# 'usedns':init_usedns
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
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
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
	# init_backend = ''
	# init_usedns = ''
	init_jail_name = ''
	init_jail_desc = ''
	init_jail_data = ''
#	init_jail_actionvars = ''
	init_jail_filter = ''
	init_jail_action = ''
	init_logpath = ''
	init_enabled = ''

	for i in qset:
		init_ignoreip = i.ignoreip
		init_bantime = i.bantime
		init_findtime = i.findtime
		init_maxretry = i.maxretry
		# init_backend = i.backend
		# init_usedns = i.usedns
		init_jail_name = i.jail_name
		init_jail_desc = i.jail_desc
		init_jail_data = i.jail_data
#		init_jail_actionvars = i.jail_actionvars
		init_jail_filter = i.jail_filter
		init_jail_action = i.jail_action
		init_logpath = i.logpath
		init_enabled = i.enabled
	form = JailEditForm(request.POST or None, initial={'ignoreip': init_ignoreip, \
		'bantime':init_bantime,\
		'findtime':init_findtime,\
		'maxretry':init_maxretry,\
		# 'backend':init_backend,\
		# 'usedns':init_usedns,\
		'jail_name':init_jail_name,\
		'jail_desc':init_jail_desc,\
		'jail_data':init_jail_data,\
#		'jail_actionvars':init_jail_actionvars,\
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
				# backend = form.cleaned_data.get("backend"),\
				# usedns = form.cleaned_data.get("usedns"),\
				jail_name = form.cleaned_data.get("jail_name"),\
				jail_desc = form.cleaned_data.get("jail_desc"),\
				jail_data = form.cleaned_data.get("jail_data"),\
#				jail_actionvars = form.cleaned_data.get("jail_actionvars"),\
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
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	context =  {
		'tlist': Jail.objects.order_by('jail_name'),
	}
	return render(request, 'manage_jails.html', context)

def view_jail(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
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
		# data += 'backend = '+i.backend +'<br>'
		# data += 'usedns = '+i.usedns+'<br>'
		data += 'filter = '+str(i.jail_filter)+'<br>'
#		data += 'action = '+str(i.jail_action) +'['+i.jail_actionvars+']<br>'
		data += 'logpath = '+i.logpath +'<br>'
		data += i.jail_data
	context = {
		'name' : name,
		'data' : mark_safe(data),
	}
	return render(request, 'view.html', context)

def delete_jail(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	name = request.GET.get('name')
	qset = Jail.objects.filter(jail_name=name)
	if qset.count() < 1:
		raise Exception('Jail entry with the given name doesn\'t exist')
	elif qset.count() > 1:
		raise Exception('More than one jails with the given name exists')
	qset.delete()
	return render(request, 'empty.html', {})

def add_customfilter(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	default_failregex = ''
	form = CustomFilterForm(request.POST or None, initial={'failregex': default_failregex})
	context =  {
		'form': form,
		'name_error': '0',
	}
	if request.method == "POST":
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/managecustomfilters/')
		else:
			if CustomFilter.objects.filter(filter_name=form.data['filter_name']).count() > 0:
				context['name_error']='1'
	return render(request,"add_customfilter.html", context)

def edit_customfilter(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	init_name = ''
	init_data = ''
	init_desc = ''
	init_fail = ''
	init_ignore = ''
	req = request.GET
	name = req.get('name')
	qset = CustomFilter.objects.filter(filter_name=name)
	if qset.count() < 1:
		raise Exception('Filter entry with the given name doesn\'t exist')
	elif qset.count() > 1:
		raise Exception('More than one filters with the given name exists')
	for i in qset:
		init_name = i.filter_name
		init_data = i.filter_data
		init_desc = i.filter_desc
		init_fail = i.failregex
		init_ignore = i.ignoreregex
	form = CustomFilterEditForm(request.POST or None, initial={'filter_name': init_name, \
		'filter_desc': init_desc, 'filter_data': init_data, 'failregex': init_fail, \
		'ignoreregex': init_ignore})
	context =  {
		'form': form,
		'name_error': '0',
	}
	if request.method == "POST":
		if form.is_valid():
			name_data = form.cleaned_data.get("filter_name")
			desc_data = form.cleaned_data.get("filter_desc")
			fail_data = form.cleaned_data.get("failregex")
			ignore_data = form.cleaned_data.get("ignoreregex")
			data_data = form.cleaned_data.get("filter_data")
			# print name_data			# print desc_data    # print data_data
			try:
				qset.update(filter_name=name_data, filter_desc=desc_data, filter_data=data_data,\
					failregex=fail_data, ignoreregex=ignore_data)
				return HttpResponseRedirect('/managecustomfilters/')
			except IntegrityError as e:
				context['name_error']='1'
		else:
			pass
	return render(request,"edit_customfilter.html", context)

def manage_customfilters(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	context =  {
		'tlist': CustomFilter.objects.order_by('filter_name'),
	}
	return render(request, 'manage_filters.html', context)

def view_customfilter(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	name = request.GET.get('name')
	qset = CustomFilter.objects.filter(filter_name=name)
	if qset.count() < 1:
		raise Exception('Filter entry with the given name doesn\'t exist')
	elif qset.count() > 1:
		raise Exception('More than one filters with the given name exists')
	data = ''
	for i in qset:
		data = i.filter_data
		fail = i.failregex
		ignore = i.ignoreregex
	context = {
		'name' : name,
		'data' : mark_safe('Fail Regex : '+ fail.replace('^%','<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;^%') + '<br><br>' + 'Ignore Regex : ' + ignore.replace('^%','<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;^%') \
		 + '<br><br>' + data),
	}
	return render(request, 'view.html', context)

def delete_customfilter(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	name = request.GET.get('name')
	qset = CustomFilter.objects.filter(filter_name=name)
	if qset.count() < 1:
		raise Exception('Filter entry with the given name doesn\'t exist')
	elif qset.count() > 1:
		raise Exception('More than one filters with the given name exists')
	qset.delete()
	return render(request, 'empty.html', {})

def add_customaction(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	form = CustomActionForm(request.POST or None, initial={'block_type': 'iptables', 'tcp_file': '/etc/hosts.deny'})
	context =  {
		'form': form,
		'name_error': '0',
	}
	if request.method == "POST":
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/managecustomactions/')
		else:
			if CustomAction.objects.filter(action_name=form.data['action_name']).count() > 0:
				context['name_error']='1'
	return render(request,"add_customaction.html", context)

def edit_customaction(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	init_name = ''
	init_data = ''
	init_desc = ''
	init_block_type = ''
	init_ip_chain = ''
	init_ip_block_type = ''
	init_ip_port = ''
	init_ip_protocol = ''
	init_tcp_file = ''
	init_tcp_block_type = ''
	req = request.GET
	name = req.get('name')
	qset = CustomAction.objects.filter(action_name=name)
	if qset.count() < 1:
		raise Exception('Action entry with the given name doesn\'t exist')
	elif qset.count() > 1:
		raise Exception('More than one actions with the given name exists')
	for i in qset:
		init_name = i.action_name
		init_data = i.action_data
		init_desc = i.action_desc
		init_block_type = i.block_type
		init_ip_chain = i.ip_chain
		init_ip_block_type = i.ip_block_type
		init_ip_port = i.ip_port
		init_ip_protocol = i.ip_protocol
		init_tcp_file = i.tcp_file
		init_tcp_block_type = i.tcp_block_type
	form = CustomActionEditForm(request.POST or None, initial={'action_name': init_name, \
		'action_desc': init_desc, 'action_data': init_data, \
		'block_type': init_block_type, \
		'ip_chain': init_ip_chain, \
		'ip_block_type': init_ip_block_type, \
		'ip_port': init_ip_port, \
		'ip_protocol': init_ip_protocol, \
		'tcp_file': init_tcp_file, \
		'tcp_block_type': init_tcp_block_type, })
	context =  {
		'form': form,
		'name_error': '0',
	}
	if request.method == "POST":
		if form.is_valid():
			name_data = form.cleaned_data.get("action_name")
			desc_data = form.cleaned_data.get("action_desc")
			data_data = form.cleaned_data.get("action_data")
			block_type_data = form.cleaned_data.get("block_type")
			ip_chain_data = form.cleaned_data.get("ip_chain")
			ip_block_type_data = form.cleaned_data.get("ip_block_type")
			ip_port_data = form.cleaned_data.get("ip_port")
			ip_protocol_data = form.cleaned_data.get("ip_protocol")
			tcp_file_data = form.cleaned_data.get("tcp_file")
			tcp_block_type_data = form.cleaned_data.get("tcp_block_type")
			# print name_data			# print desc_data    # print data_data
			try:
				qset.update(action_name=name_data, action_desc=desc_data, action_data=data_data,\
					block_type=block_type_data,\
					ip_chain=ip_chain_data,\
					ip_port=ip_port_data,\
					ip_protocol=ip_protocol_data,\
					ip_block_type=ip_block_type_data,\
					tcp_file=tcp_file_data,\
					tcp_block_type=tcp_block_type_data)
				return HttpResponseRedirect('/managecustomactions/')
			except IntegrityError as e:
				context['name_error']='1'
		else:
			pass
	return render(request,"edit_customaction.html", context)

def manage_customactions(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	context =  {
		'tlist': CustomAction.objects.order_by('action_name'),
	}
	return render(request, 'manage_actions.html', context)

def view_customaction(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	name = request.GET.get('name')
	qset = CustomAction.objects.filter(action_name=name)
	if qset.count() < 1:
		raise Exception('Action entry with the given name doesn\'t exist')
	elif qset.count() > 1:
		raise Exception('More than one actions with the given name exists')
	act_data = ''
	for i in qset:
		data = i.action_data
		init_block_type = i.block_type
		init_ip_chain = i.ip_chain
		init_ip_block_type = i.ip_block_type
		init_ip_port = i.ip_port
		init_ip_protocol = i.ip_protocol
		init_tcp_file = i.tcp_file
		init_tcp_block_type = i.tcp_block_type
	if init_block_type == 'iptables':
		act_data += 'Block Using : '+ init_block_type + '<br>'
		act_data += 'Chain Name : '+ init_ip_chain + '<br>'
		act_data += 'Block Type : '+ init_ip_block_type + '<br>'
		act_data += 'Port : '+ init_ip_port + '<br>'
		act_data += 'Protocol : '+ init_ip_protocol + '<br>'
		act_data += data + '<br><br>'
	elif init_block_type == 'tcp-wrapper':
		act_data += 'Block Using : '+ init_block_type + '<br>'
		act_data += 'TCP block file : '+ init_tcp_file + '<br>'
		act_data += 'Block Type : '+ init_tcp_block_type + '<br>'
		act_data += data + '<br><br>'
	context = {
		'name' : name,
		'data' : mark_safe(act_data),
	}
	return render(request, 'view.html', context)

def delete_customaction(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	name = request.GET.get('name')
	qset = CustomAction.objects.filter(action_name=name)
	if qset.count() < 1:
		raise Exception('Action entry with the given name doesn\'t exist')
	elif qset.count() > 1:
		raise Exception('More than one actions with the given name exists')
	qset.delete()
	return render(request, 'empty.html', {})


def add_host(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	form = HostForm(request.POST or None)
	context =  {
		'form': form,
		'name_error': '0',
	}
	if request.method == "POST":
		if form.is_valid():
			instance = form.save(commit=False)
			host_name = form.cleaned_data.get('host_name')
			jail_names = form.cleaned_data.get('jail')
			instance.ip = form.cleaned_data.get('ip')
			instance.host_name = host_name
			instance.save()
			host = Host.objects.get(host_name=host_name)
			for jail_name in jail_names:
				jailobj = Jail.objects.get(jail_name=jail_name)
				addJailRemote(host.ip, jailobj)
				# if succesful
				Membership.objects.create(host=Host.objects.get(host_name=host_name), \
					jail=Jail.objects.get(jail_name=jail_name))
			remote_fail_restart(host.ip)
			return HttpResponseRedirect('/managehosts/')
		else:
			if Host.objects.filter(host_name=form.data['host_name']).count() > 0:
				context['name_error']='1'
	return render(request,"add_host.html", context)

def edit_host(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	req = request.GET
	name = req.get('name')
	print name
	host = Host.objects.get(host_name=name)
	init_name = host.host_name
	init_ip = host.ip
	init_days = host.days
	init_jail = host.jail
	print init_jail.all()
	form = HostEditForm(request.POST or None, initial={'host_name':init_name,\
		'ip':init_ip, 'days':init_days, 'jail':init_jail.all()})
	context =  {
		'form': form,
		'name_error': '0',
	}
	if request.method == "POST":
		if form.is_valid():
			name_data = form.cleaned_data.get("host_name")
			ip_data = form.cleaned_data.get("ip")
			days_data = form.cleaned_data.get("days")
			jail_data = form.cleaned_data.get("jail")
			# print name_data			# print desc_data    # print data_data
			try:
				Host.objects.filter(host_name=name).update(host_name=name_data, ip=ip_data, days=days_data)
				delset = set(init_jail.all()).difference(set(jail_data))
				addset = set(jail_data).difference(set(init_jail.all()))
				qset = Membership.objects.filter(host=host)
				for oldjail in delset:
					oldjailobj = Jail.objects.get(jail_name=oldjail)
					delJailRemote(host.ip, oldjailobj)
					#if succesful
					qset.filter(jail=oldjailobj).delete()
				for newjail in addset:
					newjailobj = Jail.objects.get(jail_name=newjail)
					addJailRemote(host.ip, newjailobj)
					#if succesful
					Membership.objects.create(host=host, jail=newjailobj)
				remote_fail_restart(host.ip)
				return HttpResponseRedirect('/managehosts/')
			except IntegrityError as e:
				context['name_error']='1'
		else:
			pass
	return render(request,"edit_host.html", context)

def view_log(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	name = request.GET.get('name')
	qset = Host.objects.filter(host_name=name)
	if qset.count() < 1:
		raise Exception('host entry with the given name or ip doesn\'t exist')
	elif qset.count() > 1:
		raise Exception('More than one hosts with the given name or ip exists')
	data = ''
	for i in qset:
		log = i.log
	context = {
		'name' : name + 'Log',
		'data' : mark_safe(log),
	}
	return render(request, 'view.html', context)

def delete_host(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	name = request.GET.get('name')
	qset = Host.objects.filter(host_name=name)
	if qset.count() < 1:
		raise Exception('Host entry with the given name doesn\'t exist')
	elif qset.count() > 1:
		raise Exception('More than one hosts with the given name or ip exists')
	host = Host.objects.get(host_name=name)
	delset = Membership.objects.filter(host=Host.objects.get(host_name=name))
	for i in delset:
		delJailRemote(host.ip, i.jail)
	remote_fail_restart(host.ip)
	#if success
	qset.delete()
	return render(request, 'empty.html', {})

def manage_hosts(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	context =  {
		'tlist': Host.objects.order_by('host_name'),
	}
	return render(request, 'manage_hosts.html', context)

def get_log(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	name = request.GET.get('name')
	qset = Host.objects.filter(host_name=name)
	if qset.count() < 1:
		raise Exception('host entry with the given name or ip doesn\'t exist')
	elif qset.count() > 1:
		raise Exception('More than one hosts with the given name or ip exists')
	data = ''
	for i in qset:
		host_name = i.host_name
		ip = i.ip
	#fetch log(host_name,ip)
	#if not raise error
	qset.update(log='test', updated=datetime.datetime.now())
	return render(request, 'empty.html', {})

def multi_add(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	form = MultiAddForm(request.POST or None)
	context =  {
		'form': form,
	}
	if request.method == "POST":
		if form.is_valid():
			host_names = form.cleaned_data.get('host')
			jail_names = form.cleaned_data.get('jail')

			for host_name in host_names:
				host = Host.objects.get(host_name=host_name)
				for jail_name in jail_names:
					try :
						jail=Jail.objects.get(jail_name=jail_name)
						Membership.objects.create(host=host,jail=jail)
						addJailRemote(host.ip, jail)
					except Exception as e:
						pass
			return HttpResponseRedirect('/managehosts/')
		else:
			if Host.objects.filter(host_name=form.data['host_name']).count() > 0:
				context['name_error']='1'
	return render(request,"add_host.html", context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def deploylocal(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	onDeploy()
	return HttpResponseRedirect('/managehosts/')

def viewloglocal(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	os.system('./f2bmanager/suids/getlog')
	log = ''
	f = open('/tmp/fail2ban/fail2ban.log', 'r')
	lines = f.readlines()
	f.close()
	for line in lines:
		log += line + '<br>'
	context = {
		'name' : 'Log',
		'data' : mark_safe(log),
	}
	return render(request, 'view.html', context)