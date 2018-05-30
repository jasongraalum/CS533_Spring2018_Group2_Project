#!/bin/bash


# Get a list of all files beginning with "case" but not *.cpp files
tests=`ls -1 case* | grep -v cpp`

# Loop on list of test cases
for test in $tests
do
    time perf stat -d -d -d -d ./$test 4096 $loop_cout 8 > $test.out
done
