# update_cfg_conf.py

def f_fmt(val, places=1):
    'Format value to fixed number of decimal places'
    float_fmt = '%%.0%sf' % places
    return float_fmt % val

# True for test files, False for live
TESTING = False

CONF_DIR_PATH = '/home/pi/klipper_config/include' if not TESTING else '.' # Klipper destination configuration path
BLT_FNAME = 'bltouch.cfg'
SCREW_FNAME = 'screws_tilt_adjust.cfg'
ZT_FNAME = 'z_tilt.cfg'

# general options
X_OFF = -25.9
Y_OFF = -1.9
BED_X_MAX = 235
BED_Y_MAX = 235
ZT_X_MARGIN = 15

# [screws_tilt_adjust] options
SCREW_X_MIN = 29.8
#SCREW_X_MAX = 200.3
SCREW_X_MAX = 197.9
SCREW_Y_MIN = 31.3
SCREW_Y_MAX = 199.5

SCREW_HORIZ_MOVE_Z = 5
SCREW_SPEED = 75
SCREW_THREAD = 'CW-M4'

# [bltouch] options
BLT_SENSOR_PIN = '^PE4'
BLT_CONTROL_PIN = 'PE5'
BLT_HOME_X_POS = BED_X_MAX / 2.0
BLT_HOME_Y_POS = BED_Y_MAX / 2.0
BLT_Z_HOP = 5
BLT_Z_HOP_SPEED = 5

# [mesh] options
MESH_SPEED = 120
MESH_HORIZ_MOVE_Z = 5
MESH_MARGIN = 10
MESH_PROBE_CNT_X = 5
MESH_PROBE_CNT_Y = 5
MESH_ALG = 'bicubic'
MESH_FADE_START = 1
MESH_FADE_END = 10
MESH_FADE_TARGET = 0

# [z_tilt] options
ZT_STEPPER_X_DIST = 289
ZT_SPEED = 75
ZT_HORIZ_MOVE_Z = 5
ZT_RETRIES = 10
ZT_RETRY_TOLERANCE = 0.125

#######
# Do not change anything below or the script may break
#######

OUTFILES_TEST = {
    'BLT': '%s.new' % BLT_FNAME,
    'SCREW': '%s.new' % SCREW_FNAME,
    'ZT': '%s.new' % ZT_FNAME
}
OUTFILES_LIVE = {
    'BLT': '%s/%s' % (CONF_DIR_PATH, BLT_FNAME),
    'SCREW': '%s/%s' % (CONF_DIR_PATH, SCREW_FNAME),
    'ZT': '%s/%s' % (CONF_DIR_PATH, ZT_FNAME)
}

SCREW_HEADER = """
# screws approx. 170 mm apart
# 235 mm square bed
# used (x,y) diffs of %s, %s
# FL raw (%s, %s)
# RR raw = (%s, %s)
# ** subtract x and y offsets from measured values **
""" % (
        f_fmt(SCREW_X_MAX - SCREW_X_MIN), f_fmt(SCREW_Y_MAX - SCREW_Y_MIN),
        SCREW_X_MIN, SCREW_Y_MIN, SCREW_X_MAX, SCREW_Y_MAX
    )

ZT_BED_X_MIDPT = BED_X_MAX / 2.0
ZT_BED_Y_MIDPT = BED_Y_MAX / 2.0
ZT_STEPPER_X_MIDPT = ZT_STEPPER_X_DIST / 2.0
