from __future__ import unicode_literals

from django.apps import AppConfig



class F2BmanagerConfig(AppConfig):
	
    name = 'f2bmanager'
    def ready(self):
        modelname = self.get_model('DefaultJail')
        #print 'test'
        if modelname.objects.all().count() != 1:
        	modelname.objects.all().delete()
        	p = modelname()
        	p.save()

