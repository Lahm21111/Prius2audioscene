#!/bin/bash

docker build --pull --rm --build-arg USER_UID=$UID -f '.devcontainer/Dockerfile' -t 'Prius2audioscene:latest' '.' 