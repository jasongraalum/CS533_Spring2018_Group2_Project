#!/bin/bash


# Get a list of all files beginning with "case" but not *.cpp files
tests=`ls -1 case* | grep -v cpp`

# Loop on list of test cases
for test in $tests
do
  echo $test
done
