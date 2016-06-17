from django.contrib import admin

# Register your models here.

from .models import Filter
from .models import Action

class FilterAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "created", "updated"]
	class Meta:
		model = Filter

class ActionAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "description", "created", "updated"]
	class Meta:
		model = Action

admin.site.register(Filter, FilterAdmin)
admin.site.register(Action, ActionAdmin)

