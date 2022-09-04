#!/usr/bin/env python3
# send_filament_error_email.py
# Send email when filament sensor is triggered
# Created February 21, 2022
# Modified February 21, 2022

import sys
import requests as req
from datetime import datetime as dt, timedelta as td
from klipper_email_cfg import * 
from send_email import send_mail
from send_msg_to_mqtt import send_mqtt

URL = 'http://localhost:7125'
LOC_PRINT_STATS = '/printer/objects/query?print_stats'
LOC_GCODE_METADATA = '/server/files/metadata?filename=%s'

TOPIC = 'ha/basement/printer/filament_error'

def main():
    res = req.get(url=URL + LOC_PRINT_STATS)

    try:
        ps_data = res.json()['result']['status']['print_stats']
    except:
        print('Failed to load print_stats data.')
        print('Raw response: ' % res.text)
        sys.exit()

    job_name = ps_data['filename']
    job_total_duration = ps_data['total_duration']

    res = req.get(url=URL + LOC_GCODE_METADATA % job_name)

    curr_time =dt.strftime(
        dt.now(), TIME_FORMAT
    )

    body = 'To: %s\n' % DEST_EMAIL
    body += 'From: %s\n' % DEST_EMAIL
    body += 'Subject: Print job "%s" incomplete -- Runout sensor triggered @ %s\n\n' % (
            job_name, curr_time
        )
    
    f_msg_1 = 'Filament error sensor triggered for job %s' % (
        job_name
    )
    f_msg_2 = 'Job paused at %s' % (
        curr_time
    )
    
    body += f_msg_1 + '\n' + f_msg_2
    mqtt_msg = '{"state": "on", "msg": "%s\\n%s"}' % (f_msg_1, f_msg_2)
    
    print('Publishing "%s" to topic %s' % (mqtt_msg, TOPIC))

    send_mqtt(TOPIC, mqtt_msg, retain=False)

    print('Sending filament error sensor email.')

    send_mail(body)

if __name__ == '__main__':
    main()
