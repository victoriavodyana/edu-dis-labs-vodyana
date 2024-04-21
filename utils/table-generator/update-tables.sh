#!/bin/sh

mkdir -p tables/
./convert.py use-cases/* -nv -d tables/

if [ -f tables.md ]; then
    rm tables.md
fi

for i in tables/*; do
    cat $i >> tables.md
    echo "" >> tables.md
done
