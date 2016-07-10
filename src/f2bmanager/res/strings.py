class Res:
	
	filter_sshd = '# Fail2Ban filter for openssh\n#\n\n[INCLUDES]\n\n# Read comm\
on prefixes. If any customizations available -- read them from\n# common.local\nbefor\
e = common.conf\n\n\n[Definition]\n\n_daemon = sshd\n\nfailregex = <<failregex>>\n\nignor\
eregex = <<ignoreregex>>\n\n# DEV Notes:\n#\n#   "Failed \S+ for .*? from <HOST>..." failre\
gex uses non-greedy catch-all because\n#   it is coming before use of <HOST> which is not h\
ard-anchored at the end as well,\n#   and later catch-all\'s could contain user-provided in\
put, which need to be greedily\n#   matched away first.\n#\n# Author: Cyril Jaquier, Yaro\
slav Halchenko, Petr Voralek, Daniel Black'

	action_iptables = '# Fail2Ban configuration file\n#\n# Author: Cyril Ja\
quier\n#\n#\n\n[INCLUDES]\n\nbefore = iptables-blocktype.conf\n\n[Definitio\
n]\n\n# Option:  actionstart\n# Notes.:  command executed once at the start of Fail2\
Ban.\n# Values:  CMD\n#\nactionstart = iptables -N fail2ban-<name>\n              iptab\
les -A fail2ban-<name> -j RETURN\n              iptables -I <chain> -p <protocol> --\
dport <port> -j fail2ban-<name>\n\n# Option:  actionstop\n# Notes.:  command executed on\
ce at the end of Fail2Ban\n# Values:  CMD\n#\nactionstop = iptables -D <chain> -p <prot\
ocol> --dport <port> -j fail2ban-<name>\n             iptables -F fail2ban-<nam\
e>\n             iptables -X fail2ban-<name>\n\n# Option:  actioncheck\n# Notes.:  comm\
and executed once before each actionban command\n# Values:  CMD\n#\nactioncheck = ipt\
ables -n -L <chain> | grep -q \'fail2ban-<name>[ \t]\'\n\n# Option:  actionban\n# Not\
es.:  command executed when banning an IP. Take care that the\n#          command is execu\
ted with Fail2Ban user rights.\n# Tags:    See jail.conf(5) man page\n# Values:  CMD\n#\nacti\
onban = iptables -I fail2ban-<name> 1 -s <ip> -j <blocktype>\n\n# Option:  actionun\
ban\n# Notes.:  command executed when unbanning an IP. Take care that the\n#          co\
mmand is executed with Fail2Ban user rights.\n# Tags:    See jail.conf(5) man page\n# Valu\
es:  CMD\n#\nactionunban = iptables -D fail2ban-<name> -s <ip> -j <blocktype>\n\n[Ini\
t]\n\n# Default name of the chain\n#\nname = default\n\n# Option:  port\n# Notes.:  speci\
fies port to monitor\n# Values:  [ NUM | STRING ]  Default:\n#\nport = ssh\n\n# Option:  pr\
otocol\n# Notes.:  internally used by config reader for interpolations.\n# Va\
lues:  [ tcp | udp | icmp | all ] Default: tcp\n#\nprotocol = tcp\n\n# Option:  chai\
n\n# Notes    specifies the iptables chain to which the fail2ban rules should be\n#          a\
dded\n# Values:  STRING  Default: INPUT\nchain = INPUT'