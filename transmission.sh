#!/bin/bash

if [ "$1" != "" ]; then
    echo "Downloading from magnet link"
    transmission-remote -n 'transmission:transmission' -a "$1"

else
    echo "No magnet link found"
fi