#!/usr/bin/env python3

# Send email when print job completes
#
## Requires ssmtp package
## See https://github.com/th33xitus/kiauh/blob/master/docs/gcode_shell_command.md
#
# Created February 1, 2022
# Modified September 3, 2022

import sys
import requests as req
from datetime import datetime as dt, timedelta
from klipper_email_cfg import * 
from send_email import send_mail

URL = 'http://localhost:7125'
LOC_PRINT_STATS = '/printer/objects/query?print_stats'
LOC_GCODE_METADATA = '/server/files/metadata?filename=%s'

# see https://miguendes.me/how-to-use-datetimetimedelta-in-python-with-examples#heading-how-to-format-a-timedelta-as-string
def format_timedelta(delta: timedelta) -> str:
    """Formats a timedelta duration to [N days] %H:%M:%S format"""
    seconds = int(delta.total_seconds())

    secs_in_a_day = 86400
    secs_in_a_hour = 3600
    secs_in_a_min = 60

    days, seconds = divmod(seconds, secs_in_a_day)
    hours, seconds = divmod(seconds, secs_in_a_hour)
    minutes, seconds = divmod(seconds, secs_in_a_min)

    time_fmt = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    if days > 0:
        suffix = "s" if days > 1 else ""
        return f"{days} day{suffix} {time_fmt}"

    return time_fmt

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

    pst = gc_data['print_start_time']

    try:
        job_start_time_dt = dt.fromtimestamp(pst)
        job_start_time = dt.strftime(
            job_start_time_dt, TIME_FORMAT
        )
    except TypeError as e:
        print('Cannot parse %s into a datetime object: %s' %
            (pst, e))
        job_start_time = 'Unknown'

    job_end_time_dt = dt.now()
    job_end_time = dt.strftime(
        job_end_time_dt, TIME_FORMAT
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
    body += 'Duration: %s' % (
        format_timedelta(job_end_time_dt - job_start_time_dt)
    )
    print('Sending job completion email for %s' % job_name)

    send_mail(body)

if __name__ == '__main__':
    main()
