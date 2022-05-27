#!/usr/bin/env python3

import argparse, sys
from time import sleep
import paho.mqtt.client as mqtt
import mqtt_cred


USER = mqtt_cred.USER
PASS = mqtt_cred.PASS
BROKER = mqtt_cred.BROKER
BROKER_PORT = mqtt_cred.PORT
MAX_ATTEMPTS = 3

def send_mqtt(topic, status, retain=False):
    client = mqtt.Client()
    client.username_pw_set(username=USER, password=PASS)

    print('Sending status = %s to MQTT %s topic (retain = %s)' % (status, topic, retain))
    
    count = 1
    done = False
    while count <= MAX_ATTEMPTS and not done:
        try:
            client.connect(BROKER, BROKER_PORT, 60)
            client.publish(topic, status, retain=retain) # 'on or 'off'
            client.disconnect()
            done = True
        except:
            print('Attempt %d of %d failed.' % (count, MAX_ATTEMPTS))
            count += 1
            sleep(15)

def handle_error(topic, status):
    print('Failure to publish status %s to %s topic' % (status, topic), file=sys.stderr)

def main():
    my_parser = argparse.ArgumentParser(description='Send status message to MQTT Broker')

    my_parser.add_argument('topic_arg',
                           metavar='topic',
                           type=str,
                           help='MQTT topic to publish status message')

    my_parser.add_argument('status_arg',
                           metavar='status',
                           type=str,
                           help='Status to send')

    my_parser.add_argument('--retain_arg',
                          metavar='retain',
                          type=str,
                          default='F',
                          help='Retain state (default=F)')

    args = my_parser.parse_args()
    topic = args.topic_arg
    status = args.status_arg
    retain_str = args.retain_arg.upper()

    if status == '' or status is None:
        print('Invalid Status')
        sys.exit()
    elif topic == '' or topic is None:
        print('Invalid MQTT topic')
    elif retain_str not in ['T', 'F']:
        print('Retain must be T or F')
    else:
        retain = True if retain_str == 'T' else False

        
        try:
            send_mqtt(topic, status, retain=retain)
        except:
            handle_error(topic, status)

if __name__ == '__main__':
    main()
