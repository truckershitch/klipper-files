#!/bin/bash
ENDER_POWER_TOPIC="cmnd/basement/ender3v2/power"

echo "Be sure that you have compiled klipper for the SKR-2"

sleep 2
read -p "Press any key to continue..." -n1 -s

echo
echo "Powering <<ON>> Printer via MQTT"
send_msg_to_mqtt.py $ENDER_POWER_TOPIC 1

echo "Sleeping 15 seconds"
sleep 15

echo "Stopping klipper service"
sudo systemctl stop klipper.service

echo "Modifiying klipper source to enable SKR-2 flashing"
mod_klipper_src.sh

echo
echo "Flashing SKR-2"
flash_skr2.sh
