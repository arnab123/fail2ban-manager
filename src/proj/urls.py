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
    url(r'^$', views.home, name='home'),
]
