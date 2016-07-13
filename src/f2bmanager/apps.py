from __future__ import unicode_literals

from django.apps import AppConfig

import os

class F2BmanagerConfig(AppConfig):
	
    name = 'f2bmanager'
    def ready(self):
    	os.system("mkdir /tmp/fail2ban")
    	os.system("mkdir /tmp/fail2ban/filter.d")
    	os.system("mkdir /tmp/fail2ban/action.d")
    	os.system("mkdir /tmp/fail2ban/jail.d")
        modelname = self.get_model('DefaultJail')
        #print 'test'
        if modelname.objects.all().count() != 1:
        	modelname.objects.all().delete()
        	p = modelname()
        	p.save()

