from django.contrib import admin

#Register your models here.

from .forms import FilterForm
from .forms import ActionForm

from .models import Filter
from .models import Action


class FilterAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "description", "created", "updated"]
	form = FilterForm
	#class Meta:
	#	model = Filter

class ActionAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "description", "created", "updated"]
	form = ActionForm
	#class Meta:
	#	model = Action

admin.site.register(Filter, FilterAdmin)
admin.site.register(Action, ActionAdmin)
'''
'''