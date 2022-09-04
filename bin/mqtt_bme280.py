#!/usr/bin/env python3

import json
import sys
import read_bme
import send_msg_to_mqtt

TOPIC = 'basement/weather'
conds = ''
packet = '{}'

#try:
#    conds = read_bme.read_bme280()
#except Exception as e:
#    print('Error reading BME280: %s' % e)
#    sys.exit()

conds = read_bme.read_bme280()

#try:
#    packet = json.dumps(conds)
#except json.JSONDecodeError as e:
#    print('Error creating JSON: %s' % e)
#    sys.exit()

packet = json.dumps(conds)

try:
    send_msg_to_mqtt.send_mqtt(topic=TOPIC, status=packet, retain=False)
except:
    send_msg_to_mqtt.handle_error(topic=TOPIC, status=packet)
