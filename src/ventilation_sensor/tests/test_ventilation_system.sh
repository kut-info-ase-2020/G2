#!/bin/sh

test_cases=`ls tests/cases/ventilation_system/*`
for test_case in $test_cases
do
    input=`head -n 1 $test_case`
    echo $input
    output=`python3 -m tests.test_ventilation_system_executor $input 2> /dev/null`
    output_expected=`tail -n 1 $test_case`
    if [ "$output" != "$output_expected" ] ; then
        echo "case $test_case failed"
        echo "expected $output_expected"
        echo "returned $output"
        exit 1
    else
        echo pass
    fi
done
