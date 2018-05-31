#!/bin/bash


# Get a list of all files beginning with "case" but not *.cpp files
tests=`ls -1 case* | grep -v cpp`
# Loop on list of test cases
for test in $tests
do
    for loop in 1000 10000 100000 1000000 1000000000
    do
        for test_run in {1..2}
        do
            ((loop_count=${loop}*1000))
            out_file=out_${test}.${loop}.${test_run}
	    if [ ! -f ${out_file} ]; then
              rm out_${test}.${loop}.${test_run}
   	    fi
            { time perf stat -d -d -d -d ./$test 4096 ${loop_count} 8 ; } &> out_${test}.${loop}.${test_run}
        done    
    done    
done
