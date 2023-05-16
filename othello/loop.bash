#!/bin/bash
for d in 2 4 6 8
do
    for h1 in 0 1 2
    do
        for h2 in 0 1 2
        do  
            python GameDriver.py alphabeta alphabeta $h1 1 $h2 1 $d $d
        done
    done
done        