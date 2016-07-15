#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
//    setuid(0); 
	system("cp /var/log/fail2ban.log /tmp/fail2ban");
	system("chmod 775 /tmp/fail2ban/fail2ban.log");
	return 0;
}
