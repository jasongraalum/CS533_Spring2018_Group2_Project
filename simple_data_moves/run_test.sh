#!/bin/bash

# Get a list of all files beginning with "case" but not *.cpp files
tests=`ls -1 case* | grep -v cpp`
echo ${tests}
# Loop on list of test cases
for test in $tests
do
    for loop in 100 1000 10000 100000
    do
        for test_run in {1..2}
        do
            out_file=data/out_${test}.${loop}.${test_run}


            ((loop_count=${loop}))

            if [ -f ${out_file} ]; then
                rm ${out_file}
            fi

            echo "Enter the starting power(mAh) to start ${test_run} of test ${test} with ${loop} loops"
            read start_power

            { time /usr/src/linux/tools/perf/perf stat -d -d -d -d ./$test 4096 ${loop_count} 8 ; } &> ${out_file}

            echo "Enter the ending power(mAh)"
            read end_power

            echo "Starting Power = "${start_power} >> ${out_file}
            echo "Ending Power = "${end_power} >> ${out_file}

        done    
    done    
done
