#include<iostream>
#include<cstdlib>

// Case 3
//
// allocate memory <- this must be the same for all cases to eliminate variations
// Load a new value from LLC into L1 and then the Core register. 
// We need to access 2 times the total number of cache lines to be sure that they get
// evited between each subsequent access.
// Assign i to that value <- this will cause a Core Register to L1 transfer
// Looping on 2 x the size of L1 cache will cause a L1->LCC transfer
//
// The power measured is that of moving the data from LCC to L1 to the core and the assignment
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

    long int * arr = new long int[array_size];
    for (long int i = 0; i < loop_count; i++) {
        for (long int j = 0; j < loop_count; j++) {
            for (long int k = 0; k < array_size; k=k+loop_inc) {
                arr[i%array_size] = i;
            }
        }
    }
    for (long int i = 0; i < loop_count; i=i+loop_inc) {
    }
}
