import sys
f = open("/etc/fail2ban/jail.local",'r')
name_lis = sys.argv
lines = f.readlines()
f.close()

print "Hello"

for l in xrange(len(lines)):
	if lines[l] == '[' + name_lis[1] + ']\n':
		print 1
		break
while True:
	if name_lis[2] in lines[l+1]:
		lines[l+1] = name_lis[2] + ' = ' + str(name_lis[3]) + '\n'
		break
	l += 1	 

f = open("/etc/fail2ban/jail.local",'w')
for line in lines:
	f.write(line)

f.close()