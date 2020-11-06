#!/bin/bash

IFS=$'\n'
base=$(cd `dirname $0`; pwd)

for d in `find . -type d`; do
    #echo $d
    cd $base
    name=$d
    len=${#name}
    #echo $name
    #echo $len
    if [ $len -gt 15 ]; then
        echo $name
        echo "length bigger 14"
        cd $d
        pwd
        for i in ./*; do
            mv $i ../; 
        done
    cd $base
    rm -d $d
    fi

done
echo 'move finished'
