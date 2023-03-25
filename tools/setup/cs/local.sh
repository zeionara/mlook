#!/bin/bash

gh cs ports forward 8080:8080 -c "$1" > /dev/null 2>&1 & # port for server
gh cs ports forward 3000:3000 -c "$1" > /dev/null 2>&1 & # port for client
