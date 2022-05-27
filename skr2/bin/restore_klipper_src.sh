#!/bin/sh

BASE_FILENAME="board_defs.py"
ORIG_PATH="/home/pi/klipper/scripts/spi_flash/"
MOD_PATH="/home/pi/"
MOD_SUFFIX=".skr2"

cp ${MOD_PATH}${BASE_FILENAME} ${ORIG_PATH}

echo "Klipper source tree restored."

exit 0
