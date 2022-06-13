#include <stdio.h>

int main(void) {
    int i;

    printf("i = %d\n", i);
    printf("1234%n\n", &i);

    printf("i = %d\n", i);

    return 1;
}