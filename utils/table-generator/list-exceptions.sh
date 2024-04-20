#!/bin/sh

grep -E '\|\ [0-9]{3}\.[0-9]{3}' use-cases/*.uc \
    | cut -d '|' -f 2 \
    | sort | uniq -c
