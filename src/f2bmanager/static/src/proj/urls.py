"""proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from f2bmanager import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^manager/', views.get_manager, name='manager'),
    url(r'^addfilter/', views.add_filter, name='addfilter'),
    url(r'^addaction/', views.add_action, name='addaction'),
    url(r'^editfilter/', views.edit_filter, name='editfilter'),
    url(r'^editaction/', views.edit_action, name='editaction'),
    url(r'^viewfilter/', views.view_filter, name='viewfilter'),
    url(r'^viewaction/', views.view_action, name='viewaction'),
    url(r'^deletefilter/', views.delete_filter, name='deletefilter'),
    url(r'^deleteaction/', views.delete_action, name='deleteaction'),
    url(r'^managefilters/', views.manage_filters, name='managefilters'),
    url(r'^manageactions/', views.manage_actions, name='manageactions'),
	url(r'^managejails/', views.manage_jails, name='managejails'),
	url(r'^addjail/', views.add_jail, name='addjail'),
	url(r'^editjail/', views.edit_jail, name='editjail'),
	url(r'^editdefaultjail/', views.edit_defaultjail, name='editdefaultjail'),
	url(r'^deletejail/', views.delete_jail, name='deletejail'),
	url(r'^viewjail/', views.view_jail, name='viewjail'),
	url(r'^addcustomfilter/', views.add_customfilter, name='addcustomfilter'),
    url(r'^addcustomaction/', views.add_customaction, name='addcustomaction'),
    url(r'^editcustomfilter/', views.edit_customfilter, name='editcustomfilter'),
    url(r'^editcustomaction/', views.edit_customaction, name='editcustomaction'),
    url(r'^viewcustomfilter/', views.view_customfilter, name='viewcustomfilter'),
    url(r'^viewcustomaction/', views.view_customaction, name='viewcustomaction'),
    url(r'^deletecustomfilter/', views.delete_customfilter, name='deletecustomfilter'),
    url(r'^deletecustomaction/', views.delete_customaction, name='deletecustomaction'),
    url(r'^managecustomfilters/', views.manage_customfilters, name='managecustomfilters'),
    url(r'^managecustomactions/', views.manage_customactions, name='managecustomactions'),
	url(r'^addhost/', views.add_host, name='addhost'),
	url(r'^edithost/', views.edit_host, name='edithost'),
	url(r'^managehosts/', views.manage_hosts, name='managehosts'),
	url(r'^deletehost/', views.delete_host, name='deletehost'),
	url(r'^viewlog/', views.view_log, name='viewlog'),
	url(r'^getlog/', views.get_log, name='getlog'),
	url(r'^multiadd/', views.multi_add, name='multiadd'),
	url(r'^logout/', views.logout_view, name='logout'),
	url(r'^deploylocal/', views.deploylocal, name='deploylocal'),
	url(r'^viewloglocal/', views.viewloglocal, name='viewloglocal'),
	url(r'^$', views.home, name='home'),
]
