#include <unistd.h>

int main() {
    // Create an array of character pointers to hold the argument list
    char *argv[] = {"-l"};

    // Use execve to execute the "ls" command with the argument list
    execve("/bin/ls", argv, NULL);

    // execve only returns if there is an error, so if we reach this point,
    // something went wrong
    perror("execve failed");
    return 1;
}