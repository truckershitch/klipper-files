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

URL = 'http://localhost:7125'
LOC_PRINT_STATS = '/printer/objects/query?print_stats'
LOC_GCODE_METADATA = '/server/files/metadata?filename=%s'

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
    body += 'Filament error sensor triggered for job %s\n' % (
        job_name
    )
    body += 'Job paused at %s\n' % (
        curr_time
    )

    print('Sending filament error sensor email.')

    send_mail(body)

if __name__ == '__main__':
    main()