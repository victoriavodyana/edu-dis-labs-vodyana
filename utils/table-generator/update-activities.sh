#!/bin/sh

mkdir -p activities/
./convert.py use-cases/* -a -nv -d activities/

if [ -f activities.md ]; then
    rm activities.md
fi

for i in activities/*; do
    cat $i >> activities.md
    echo "" >> activities.md
done
