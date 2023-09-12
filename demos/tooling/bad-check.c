#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

void print_flag() {
    char ch, decrypted_flag[] = "PKUOPVKQ1IYE2RKFO3ZKCCON7WI9MROMU0";
    int key = 10;

    for (int i = 0; decrypted_flag[i] != '\0'; ++i) {
        ch = decrypted_flag[i];
        if (isalnum(ch)) {
            if (islower(ch)) {
                ch = (ch - 'a' - key + 26) % 26 + 'a';
            }
            if (isupper(ch)) {
                ch = (ch - 'A' - key + 26) % 26 + 'A';
            }
            if (isdigit(ch)) {
                ch = (ch - '0' - key + 10) % 10 + '0';
                ch = '_';
            }
        } else if (ch == '_') {
           ch = ch % 49; 
        }
        decrypted_flag[i] = ch;
    }
    decrypted_flag[8] = '{';
    decrypted_flag[33] = '}';
    printf(decrypted_flag);
}

int main(int argc, char * argv[]) {
  printf("It's taken a while but I think I've finally written a secure program\n");

  int flag = 1;
  if (flag == 0) print_flag();

  return 0;
}
