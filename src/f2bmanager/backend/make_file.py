import sys
name_lis = sys.argv
f = open('/etc/fail2ban/' + name_lis[1] + '/' + name_lis[2]+'.conf','w')
f.write(name_lis[3])
f.close()