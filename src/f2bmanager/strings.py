class Res:
	
	filter_sshd = '# Fail2Ban filter for openssh\n#\n\n[INCLUDES]\n\n# Read comm\
on prefixes. If any customizations available -- read them from\n# common.local\nbefor\
e = common.conf\n\n\n[Definition]\n\n_daemon = sshd\n\nfailregex = <<failregex>>\n\nignor\
eregex = <<ignoreregex>>\n\n# DEV Notes:\n#\n#   "Failed \S+ for .*? from <HOST>..." failre\
gex uses non-greedy catch-all because\n#   it is coming before use of <HOST> which is not h\
ard-anchored at the end as well,\n#   and later catch-all\'s could contain user-provided in\
put, which need to be greedily\n#   matched away first.\n#\n# Author: Cyril Jaquier, Yaro\
slav Halchenko, Petr Voralek, Daniel Black'

	action_iptables = '# Fail2Ban configuration file\n#\n# Author: Cyril Jaquier\n#\n#\n\n[INC\
LUDES]\n\nbefore = iptables-blocktype.conf\n\n[Definition]\n\n# Option:  actionstart\n# Note\
s.:  command executed once at the start of Fail2Ban.\n# Values:  CMD\n#\nactionstart = iptab\
les -N fail2ban-<name>\n              iptables -A fail2ban-<name> -j RETURN\n              ipt\
ables -I <chain> -p <protocol> --dport <port> -j fail2ban-<name>\n\n# Option:  action\
stop\n# Notes.:  command executed once at the end of Fail2Ban\n# Values:  CMD\n#\nactions\
top = iptables -D <chain> -p <protocol> --dport <port> -j fail2ban-<name>\n             ipt\
ables -F fail2ban-<name>\n             iptables -X fail2ban-<name>\n\n# Option:  actionche\
ck\n# Notes.:  command executed once before each actionban command\n# Values:  CMD\n#\nact\
ioncheck = iptables -n -L <chain> | grep -q \'fail2ban-<name>[ \t]\'\n\n# Option:  action\
ban\n# Notes.:  command executed when banning an IP. Take care that the\n#          comman\
d is executed with Fail2Ban user rights.\n# Tags:    See jail.conf(5) man page\n# Value\
s:  CMD\n#\nactionban = iptables -I fail2ban-<name> 1 -s <ip> -j <blocktype>\n\n# Opti\
on:  actionunban\n# Notes.:  command executed when unbanning an IP. Take care that t\
he\n#          command is executed with Fail2Ban user rights.\n# Tags:    See jail.con\
f(5) man page\n# Values:  CMD\n#\nactionunban = iptables -D fail2ban-<name> -s <ip> -j <b\
locktype>\n\n[Init]\n\n# Default name of the chain\n#\nname = <<name>>\n\n# Option:  por\
t\n# Notes.:  specifies port to monitor\n# Values:  [ NUM | STRING ]  Default:\n#\npo\
rt = <<port>>\n\n# Option:  protocol\n# Notes.:  internally used by config reader for in\
terpolations.\n# Values:  [ tcp | udp | icmp | all ] Default: tcp\n#\nprotoco\
l = <<protocol>>\n\n# Option:  chain\n# Notes    specifies the iptables chain to whi\
ch the fail2ban rules should be\n#          added\n# Values:  STRING  Default: INPUT\ncha\
in = INPUT\n\nblocktype = <<blocktype>>'

	action_hostsdeny = '# Fail2Ban configuration file\n#\n# Author: Cyril Jaquier\n# Ed\
ited for cross platform by: James Stout, Yaroslav Halchenko and Daniel Black\n#\n#\n\n[Defin\
ition]\n\n# Option:  actionstart\n# Notes.:  command executed once at the start of Fail\
2Ban.\n# Values:  CMD\n#\nactionstart = \n\n# Option:  actionstop\n# Notes.:  command exec\
uted once at the end of Fail2Ban\n# Values:  CMD\n#\nactionstop = \n\n# Option:  actionc\
heck\n# Notes.:  command executed once before each actionban command\n# Values:  CMD\n#\nacti\
oncheck = \n\n# Option:  actionban\n# Notes.:  command executed when banning an IP. Take c\
are that the\n#          command is executed with Fail2Ban user rights.\n# Tags:    See ja\
il.conf(5) man page\n# Values:  CMD\n#\nactionban = IP=<ip> &&\n            printf %%b "<d\
aemon_list>: $IP\n" >> <file>\n\n# Option:  actionunban\n# Notes.:  command executed wh\
en unbanning an IP. Take care that the\n#          command is executed with Fail2Ban us\
er rights.\n# Tags:    See jail.conf(5) man page\n# Values:  CMD\n#\nactionunban = ec\
ho "/^<daemon_list>: <ip>$/<br>d<br>w<br>q" | ed <file>\n\n[Init]\n\n# Option:  fi\
le\n# Notes.:  hosts.deny file path.\n# Values:  STR  Default:  /etc/hosts.deny\n#\nfil\
e = <<file>>\n\n# Option:  daemon_list\n# Notes:   The list of services that this action w\
ill deny. See the man page\n#          for hosts.deny/hosts_access. Default is all servi\
ces.\n# Values:  STR  Default: ALL\ndaemon_list = <<blocktype>>'