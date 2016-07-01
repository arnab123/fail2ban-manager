# os.system('python f2bmanager/backend/change_name.py prev_name final_name')

import sys
f = open("/etc/fail2ban/jail.local",'r')
name_lis = sys.argv
lines = f.readlines()
f.close()

print "HI"
f = open("/etc/fail2ban/jail.local",'w')
for line in lines:
	if line == name_lis[1] + '\n':
		f.write(name_lis[2] + '\n')
	else:
		f.write(line)

f.close()