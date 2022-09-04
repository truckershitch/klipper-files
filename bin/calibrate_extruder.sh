#!/bin/sh
# Calibrate Extruder shortcut
#
# Created January 30, 2022
# Modified January 30, 2022

TEMP=250

echo "Calibrating Extruder to ${TEMP}C"
echo "PID_CALIBRATE HEATER=extruder TARGET=${TEMP}" > /tmp/printer
