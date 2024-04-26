#!/bin/bash
docker build -t terrameow .
docker run --rm -p 50002:50002 -it --name terrameow terrameow 
