#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
//    setuid(0); 
	system("cp -r /tmp/fail2ban/filter.d /etc/fail2ban");
	return 0;
}

