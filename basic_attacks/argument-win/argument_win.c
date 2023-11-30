#include <stdio.h>

__asm__("pop %rdi;"
		"pop %rsi;"
        "ret;");

int win(int a, int b){
	char* str = "/bin/sh;";
	if(a == 69 && b == 1337){
		system(str);
	}
}

int main(){
	char a[10];
	gets(a);
}