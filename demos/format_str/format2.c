#include <stdio.h>

int main(void) {
    int i;
    char buffer[50];

    printf("i = %d [%x]\n", i, &i);
    
    fgets(buffer, sizeof(buffer), stdin);
    printf(buffer);

    printf("i = %d\n", i);

    return 1;
}