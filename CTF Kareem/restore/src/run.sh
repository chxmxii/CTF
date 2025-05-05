#!/bin/bash

set -eu

cleanup() {
    docker rm -f $(docker ps -a | grep registry | awk '{print $1}') || true 
}

run() {
    docker run -d -p 5000:5000 --name restore \
        -v "$(pwd)/restore:/var/lib/registry" \
        -v "$(pwd)/config.yml:/etc/docker/registry/config.yml" \
        registry:2 serve /etc/docker/registry/config.yml
}

cleanup
run
