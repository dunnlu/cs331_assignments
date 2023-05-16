#!/bin/bash
for d in 2 4 6 8 10 12
do
    for p in 0 1
    do
        for h in 0 1 2
        do  
            python GameDriver.py alphabeta alphabeta $h $p $h $p $d $d
        done
    done
done        