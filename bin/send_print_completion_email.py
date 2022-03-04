#!/usr/bin/env python3

# Send email when print job completes
#
## Requires ssmtp package
## See https://github.com/th33xitus/kiauh/blob/master/docs/gcode_shell_command.md
#
# Created February 1, 2022
# Modified February 21, 2022

from curses import noecho
import sys
import requests as req
from datetime import datetime as dt, timedelta as td
from klipper_email_cfg import * 
from send_email import send_mail

URL = 'http://localhost:7125'
LOC_PRINT_STATS = '/printer/objects/query?print_stats'
LOC_GCODE_METADATA = '/server/files/metadata?filename=%s'

def main():
    def bad_res(name, r=None):
        print('Failed to load %s data.' % name)
        if r is not None:
            print('Raw response: %s' % r.text)
        sys.exit()

    res = req.get(url=URL + LOC_PRINT_STATS)
    if res.status_code != 200:
        bad_res('print_stats')

    try:
        ps_data = res.json()['result']['status']['print_stats']
    except:
        bad_res('print_stats', res)

    job_name = ps_data['filename']
    job_total_duration = ps_data['total_duration']

    res = req.get(url=URL + LOC_GCODE_METADATA % job_name)
    if res.status_code != 200:
        bad_res('gcode metadata')

    try:
        gc_data = res.json()['result']
    except:
        bad_res('gcode metadata', res)

    try:
        pst = gc_data['print_start_time']
        job_start_time = dt.strftime(
            dt.fromtimestamp(pst), TIME_FORMAT
        )
    except ValueError as e:
        print('Cannot parse %s into a datetime object: %s' %
            (pst, e))

    job_end_time = dt.strftime(
        dt.now(), TIME_FORMAT
    )    

    body = 'To: %s\n' % DEST_EMAIL
    body += 'From: %s\n' % DEST_EMAIL
    body += 'Subject: Print job "%s" completed\n\n' % (
            job_name
        )
    body += 'Print job: %s\nStart Time: %s\nCompleted: %s\n' % (
            job_name,
            job_start_time,
            job_end_time
        )
        #body += 'Duration: %s seconds' % (
        #     int(job_total_duration)
        # )
    print('Sending job completion email for %s' % job_name)

    send_mail(body)

if __name__ == '__main__':
    main()