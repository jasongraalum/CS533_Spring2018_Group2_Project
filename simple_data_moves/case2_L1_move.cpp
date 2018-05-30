#include<iostream>
#include<cstdlib>

// Case 2
//
// allocate memory <- this must be the same for all cases to eliminate variations
// Load a new value from L1 into the Core register. We need to alternate between two cache lines to ensure that a load is happening.
// Assign i to that value <- this will cause a Core Register to L1 transfer
// Use the same location in L1 to avoid any LLC to L1 data transfers
//
// The power measured is that of moving the data from L1 to the core and the assignment
//

int main(int argc, char ** argv) {
    // usage: program array_size loop_count loop_increment
    
    if(argc != 4)
    {
        std::cout << "Usage: program array_size loop_cout loop_increment" << std::endl;
        exit(-1);
    }
    long int array_size = strtol(argv[1],&argv[1],10);
    long int loop_count = strtol(argv[2],&argv[2],10);
    long int loop_inc = strtol(argv[3],&argv[3],10);
    int x;

    long int * arr = new long int[array_size];
    for (long int i = 0; i < loop_count; i=i+loop_inc) {
        // Alternate between two cache lines in L1
        // Loop inc should be 8
        arr[i%2] = i;
    }
}
