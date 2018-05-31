#include<iostream>
#include<cstdlib>

// Case 1 
//
// allocate memory <- this must be the same for all cases to eliminate variations
// Assign i to x loop_count times;
//
// The power measured is that of the assignment and no data movement besides the baseline
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

    for (long int i = 0; i < loop_count; i++) {
        for (long int j = 0; j < loop_count; j++) {
            for (long int k = 0; k < array_size; k=k+loop_inc) {
                x = k;
            }
        }
    }
}
