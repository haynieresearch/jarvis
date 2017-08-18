#!/bin/bash
if [[ "$(ping -c 1 8.8.8.8 | grep '100% packet loss' )" != "" ]]; then
    echo "DOWN"
    exit 1
else
    echo "UP"
    exit 0
fi
