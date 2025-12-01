#!/bin/bash

gen_ak() {
    echo "AKAI`openssl rand -base64 30 | tr -d '=+/[:lower:]' | tr '[:lower:]' '[:upper:]' | head -c 16`"
}

gen_sk() {
    openssl rand -base64 30
}

ping() {
    curl -si http://pwnsec.cloud/_localstack/health
}

run() {
    func_name=$1
    shift
    $func_name "$@"
}

run "$@"