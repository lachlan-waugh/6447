#include <stdio.h>

void main(){
	int var = 1, var_2;

	printf("It was:    %d\n", var);
	printf("_A_B_C_D_  %n\n", &var);
	printf("Now it is: %d\n", var);

	printf("_A_B_C_D_ %2$n\n", &var, &var_2);
	printf("Now it is: %2$d\n", var, var_2);
	
	printf("%n        \n", &var);
	printf("Now it is: %d\n", var);
}
