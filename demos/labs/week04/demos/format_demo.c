#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int target = 42;

void echo_input(char *input,char *password){
	fgets(input, 1000, stdin);
	printf(input);

	if(target != 42){
		printf("\n------------------------------------------------------\nYou successfully exploited the target variable!\n------------------------------------------------------\n\n");
	} else if(strncmp(input, password, strlen(password)) == 0){
		printf("\n------------------------------------------------------\nYou found the hidden password!\n------------------------------------------------------\n\n");
	}
}

int main(int argc, char **argv){
	char input[1000];
	char password[] = "___Secret_Password_Stored_on_Stack___";

	echo_input(input, password);
}

