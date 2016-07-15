#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
//    setuid(0); 
	system("fail2ban-client reload");
	return 0;
}
