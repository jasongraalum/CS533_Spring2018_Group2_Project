#include<stdio.h>

void main() {
  long int arr[4096] = {0};
  int i;
    for ( i =0; i<100000; i=+8) {
      arr[i%4096] = i;
  }
}
