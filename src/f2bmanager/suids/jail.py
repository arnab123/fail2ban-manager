from os import walk

f = []
file1 = open('/etc/fail2ban/jail.local', 'a')
for (p, d, fname) in walk('/tmp/fail2ban/jail.d'):
	f.extend(fname)
for ele in f:
	if '~' not in ele:
		f1 = open('/tmp/fail2ban/jail.d' + '/' + ele , 'r')
		t2 = f1.read()
		file1.write(t2+'\n\n')
		f1.close()
file1.close()