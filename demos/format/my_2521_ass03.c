#include <stdio.h>

int main(void) {
    char buffer[50];

    fgets(buffer, sizeof(buffer), stdin);
    printf(buffer);

    return 1;
}

// for i in `seq 1 30`; do echo "AAAA %$i\$x" | ./my_2521_ass03; done