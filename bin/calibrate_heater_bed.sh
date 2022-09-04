#!/bin/sh
# Calibrate Heater Bed shortcut
#
# Created January 30, 2022
# Modified January 30, 2022

TEMP=75

echo "Calibrating Heater Bed to ${TEMP}C"
echo "PID_CALIBRATE HEATER=heater_bed TARGET=${TEMP}" > /tmp/printer
