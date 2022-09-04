#!/bin/bash

SRC="/home/pi/gcode_files"
THUMBS=".thumbs"
DEST="/home/pi/gcode_archive"

cd ${SRC}
for f in *.gcode; do

    today=$(date +%s)
    mod_time=$(stat -c %Y "${f}")
    age=$(( ( ${today} - ${mod_time} ) / 86400 ))

    if [ ${age} > 90 ]; then
        echo "file: ${f} age: ${age}"
    fi
done

