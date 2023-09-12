#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char FLAG[] = "FAK\nEFL\nAG{\nEVE\nN_W\nHEN\n_I_\nENC\nRYP\nTED\n_TH\nE_F\nLAG\n_??\n}";

int main(void) {
  	int i, n ;
  	printf("Enter a number: ");
    scanf("%d", &n);
    for (i=1; i<=n; i++) {
        if (i % 15 == 0)        printf ("FizzBuzz\t");
        else if ((i % 3) == 0)  printf("Fizz\t");
        else if ((i % 5) == 0)  printf("Buzz\t");
        else                 	printf("%d\t", i);
    }

    return 0;
}
