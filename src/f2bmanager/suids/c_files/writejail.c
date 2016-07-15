#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
	//setuid(0); 
	system("python /home/arnab/django/proj/src/f2bmanager/suids/jail.py");
	return 0;
}

