#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>  
#include <sys/stat.h>    
#include <fcntl.h>

int main(int argc,char* argv[])
{
	int a = 5;
	char* ch = "helloword\r\n";
	int fd;
	fd = open("task.txt",O_WRONLY|O_CREAT|O_APPEND);
	while(a)
	{
		sleep(1);
		printf("sssssss\n");
		write(fd,ch,sizeof(ch));
		a--;
	}
	close(fd);
	return 0;
}
