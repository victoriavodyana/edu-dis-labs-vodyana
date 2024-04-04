#!/bin/sh

mkdir -p tables/
./convert.py use-cases/* -nv -d tables/
