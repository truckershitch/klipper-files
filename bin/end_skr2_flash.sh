#!/bin/sh
ENDER_POWER_TOPIC="cmnd/basement/ender3v2/power"

echo "Restoring Klipper Source"
restore_klipper_src.sh

echo "Powering <<OFF>> Printer via MQTT"
send_msg_to_mqtt.py $ENDER_POWER_TOPIC 0

echo "Sleeping 15 seconds"
sleep 15

echo "Powering <<ON>> Printer via MQTT"
send_msg_to_mqtt.py $ENDER_POWER_TOPIC 1

echo "Sleeping 10 seconds"
sleep 10

echo "Staring klipper service"
sudo systemctl start klipper.service
