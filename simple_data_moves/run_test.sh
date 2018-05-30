#!/bin/bash


# Get a list of all files beginning with "case" but not *.cpp files
tests =`ls -1 case* | grep -v cpp`
loop_cout = (1000 10000 100000 1000000 1000000000)
# Loop on list of test cases
for test in $tests
do
    for loop in ${loop_cout[*]}
    do
        for test_run in {1..10}
        do
            time perf stat -d -d -d -d ./$test 4096 ${loop_cout[$index]} 8 > $test.out
        done    
    done    
done
