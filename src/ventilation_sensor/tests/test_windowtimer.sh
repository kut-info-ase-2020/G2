#!/bin/bash

test_case_inputs=`ls tests/cases/windowtimer/*.input`
for test_case_input in $test_case_inputs
do
    input=`cat $test_case_input`
    output=`python3 -m tests.test_windowtimer_executor $input 2> /dev/null`
    output_filename=${test_case_input//input/output}
    output_expected=`cat $output_filename`
    if [ "$output" != "$output_expected" ] ; then
        echo "case $test_case failed"
        echo "expected $output_expected"
        echo "returned $output"
        exit 1
    else
        echo pass
    fi
done
