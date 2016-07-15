from __future__ import unicode_literals

from django.apps import AppConfig

import os

class F2BmanagerConfig(AppConfig):
	
    name = 'f2bmanager'
    def ready(self):
    	if not os.path.isdir('/tmp/fail2ban'):
    		os.system("mkdir /tmp/fail2ban")
    	if not os.path.isdir('/tmp/fail2ban/filter.d'):
    		os.system("mkdir /tmp/fail2ban/filter.d")
    	if not os.path.isdir('/tmp/fail2ban/action.d'):
    		os.system("mkdir /tmp/fail2ban/action.d")
    	if not os.path.isdir('/tmp/fail2ban/jail.d'):
    		os.system("mkdir /tmp/fail2ban/jail.d")

        try:
        	modelname = self.get_model('DefaultJail')
        	if modelname.objects.all().count() != 1:
        		modelname.objects.all().delete()
        		p = modelname()
        		p.save()
    	except Exception as e:
    		pass

