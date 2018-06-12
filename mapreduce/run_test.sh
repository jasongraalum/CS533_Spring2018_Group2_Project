#!/bin/bash

# Get a list of all files beginning with "case" but not *.cpp files
super_args={ "single", "branching", "cascade", "cascade_procs" }
echo ${super_args}
# Loop on list of test cases
for test in $super_args
do
        for test_run in {1..10}
        do
            out_file=data/mapr_out_${test}.${test_run}

            if [ -f ${out_file} ]; then
                rm ${out_file}
            fi

#            read start_power
            fswebcam -r 1280x720 --no-banner ${out_file}.start.jpg

            { time /usr/src/linux/tools/perf/perf stat -d -d -d -d python ./supervisor.py $test 180; } &> ${out_file}

#           read end_power
            fswebcam -r 1280x720 --no-banner ${out_file}.end.jpg

            echo "Starting Power = "${start_power} >> ${out_file}
            echo "Ending Power = "${end_power} >> ${out_file}

    done    
done
