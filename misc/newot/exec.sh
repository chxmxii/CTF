#!/bin/bash

while true; do
    socat TCP-LISTEN:50002,reuseaddr,fork SYSTEM:'sh entrypoint.sh'
done

