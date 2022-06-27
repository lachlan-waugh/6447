#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int one(int FLAG) {
    int flags = 1;

    if (flags & FLAG){
        printf("TRUE\n");
    } else{
        printf("FALSE\n");
    }
}

int two(int flags, int FLAG) {
    if (flags & FLAG != 0){
        printf("TRUE\n");
    } else{
        printf("FALSE\n");
    }
}

int three(int x, int y) {
    if (x == 0) {
        if (y == 0) printf("error\n");
    else {
        int z = x + y;
        printf("fclose\n");
    }
    }
}

int main(int argc, char **argv) {
    int chal = atoi(argv[1]);

    switch (chal) {
        case 1:
            one(atoi(argv[2]));
            break;
        case 2:
            two(atoi(argv[2]), atoi(argv[3]));
            break;
        case 3:
            three(atoi(argv[2]), atoi(argv[3]));
            break;
        case 4:
            
            break;
    }
}