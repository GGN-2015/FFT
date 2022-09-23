#!/bin/bash

CNT=12

I=1
while [ $I -le $CNT ] ; do
    ./auto.sh `printf "%04d" $I`
    (( I=I+1 ))
done

