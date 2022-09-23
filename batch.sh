#!/bin/bash

if [ "$1" = "" -o "$2" = "" ] ; then
    echo -e "[batch.Error] Usage: $0 \<ID_FROM\> \<ID_TO\>"
    exit 0
fi

I=$1
while [ $I -le $2 ] ; do
    ./auto.sh `printf "%04d" $I`
    (( I=I+1 ))
done

