#!/usr/bin/env python3

# Calculates new rotation distance from measured data and former
# Writes new printer configuration to default new path
# unless user chooses a new path different that the
# original printer configuration path (for safety).
#
# Created August 19, 2021
# Modified August 21, 2021

import requests
import argparse

def process_cmd_line():
    defaults = {
        'u': 'http://localhost',
        'p': 7125,
        'src': '/home/pi/klipper_config/printer.cfg',
        'dest': '/home/pi/klipper_config/printer.cfg.new'
    }

    my_parser = argparse.ArgumentParser(description='Calculate the Klipper rotation_distance parameter and optionally writes a new configuration.')

    my_parser.add_argument('i', metavar='init_mark_dist', type=float, help='Initial Mark Distance')
    my_parser.add_argument('r', metavar='req_ext_dist', type=float, help='Requested Extrude distance')
    my_parser.add_argument('s', metavar='subs_mark_dist', type=float, help='Subsequent Mark Distance')

    my_parser.add_argument('-u', metavar='--url', type=str, default=defaults['u'], help='Base URL of Moonraker Host [%s]' % defaults['u'])
    my_parser.add_argument('-p', metavar='--port', type=int, default=defaults['p'], help='Moonraker Port [%s]' % defaults['p'])
    my_parser.add_argument('-src', metavar='--source_path', type=str, default=defaults['src'], help='Full pathname of Klipper printer.cfg [%s]' % defaults['src'])
    my_parser.add_argument('-dest', metavar='--dest_path', type=str,  default=defaults['dest'], help='Destination path for new printer.cfg [%s]' % defaults['dest'])

    args = my_parser.parse_args()

    result = {
        'initial_mark_dist': args.i,
        'requested_extrude_dist': args.r,
        'subsequent_mark_dist': args.s
    }

    attribs = vars(args)
    opt_args = ['u', 'p', 'src', 'dest']

    for i in opt_args:
        if i in attribs:
            result[i] = attribs[i]
        else:
            result[i] = defaults[i]

    result['prog'] = my_parser.prog

    print('result: %s' % result)
    
    return result

def get_prev_rot_dist(url, port):
    REQ_BASE_PATH = '/printer/objects/query?'
    REQ_QUERY_STR = 'configfile=config'

    req = requests.get('%s:%d%s%s' % (url, port, REQ_BASE_PATH, REQ_QUERY_STR))
    conf_previous_rotation_dist = float(req.json()['result']['status']['configfile']['config']['extruder']['rotation_distance'])

    previous_rotation_dist = conf_previous_rotation_dist

    invalid_choice = True
    use_prev_rot_dist = ''
    while invalid_choice:
        print('Previous rotation distance pulled from printer.cfg via Moonraker API: %s' %
        (conf_previous_rotation_dist))
        use_prev_rot_dist = input('Use this value for calculation (y/n)? ')
        if use_prev_rot_dist.lower() not in ['y', 'n']:
            print('\nGet with it, buddy.  Y, y, n, N are valid choices here.\nI don\'t have all day, pal!\n')
        else:
            invalid_choice = False

    if use_prev_rot_dist == 'n':
        done = False
        while not done:
            new_prev_rot_dist_str = input('Enter the desired previous rotation distance: ')
            try:
                previous_rotation_dist = float(new_prev_rot_dist_str)
                if previous_rotation_dist > 0:
                    done = True
            except ValueError:
                print('Bad value, idiot. Must be a positive number.')

    return previous_rotation_dist

def calc_rot_dist(previous_rotation_dist, initial_mark_dist, requested_extrude_dist, subsequent_mark_dist):
    print('\nInitial Mark Distance: %s' % initial_mark_dist)
    print('Requested Extrude Distance: %s' % requested_extrude_dist)
    print('Subsequent Mark Distance: %s\n' % subsequent_mark_dist)

    # do calculations
    actual_extrude_dist = initial_mark_dist - subsequent_mark_dist
    rotation_distance = previous_rotation_dist * actual_extrude_dist / requested_extrude_dist

    print('Calculation for rotation distance in Klipper is done as follows:\n')
    print('actual_extrude_dist = initial_mark_dist - subsequent_mark_dist')
    print('%s - %s' % (initial_mark_dist, subsequent_mark_dist))
    print('actual_extrude_dist = %s\n' % actual_extrude_dist)
    print('rotation_distance = previous_rotation_dist * actual_extrude_dist / requested_extrude_dist')
    print('%s * %s / %s' % (previous_rotation_dist, actual_extrude_dist, requested_extrude_dist))
    print('rotation_distance = %s\n' % rotation_distance)

    print('New rotation distance: %.6f\n' % rotation_distance)

    return rotation_distance

def write_new_configuration(prog, rotation_distance, source_path, dest_path):
    DISCLAIMER = '# modified by %s' % prog
    new_conf_filename_okay = input('Full pathname to new printer configuration: %s\nIs this okay (y/n)? '
        % dest_path)

    if new_conf_filename_okay.lower() == 'n':
        new_path_chosen = False
        while not new_path_chosen:
            new_dest_path = input('Enter full pathname for new printer configuration.')
            if new_dest_path == source_path:
                print('PATHNAME CANNOT BE %s\nChoose a different pathname.' % source_path)
            else:
                new_path_chosen = True
    else:
        new_dest_path = dest_path

    print('\nWriting to %s' % new_dest_path)

    found = False
    target = 'rotation_distance:'

    with open(source_path, 'r') as orig_file:
        with open(new_dest_path, 'w') as new_file:
            for line in orig_file:
                l_strip = line.strip()
                if l_strip == '[extruder]':
                    found = True
                
                if found and l_strip.startswith(target):
                    new_file.write('%s %.6f %s\n' % (target, rotation_distance, DISCLAIMER))
                else:
                    new_file.write(line)

def main():
    vals = process_cmd_line()
    previous_rotation_distance = get_prev_rot_dist(vals['u'], vals['p'])
    rotation_distance = calc_rot_dist(previous_rotation_distance, vals['initial_mark_dist'], vals['requested_extrude_dist'], vals['subsequent_mark_dist'])
    write_new_configuration(vals['prog'], rotation_distance, vals['src'], vals['dest'])

if __name__ == '__main__':
    main()