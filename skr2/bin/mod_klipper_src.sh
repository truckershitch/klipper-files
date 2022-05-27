#!/bin/sh

BASE_FILENAME="board_defs.py"
ORIG_PATH="/home/pi/klipper/scripts/spi_flash/"
MOD_PATH="/home/pi/"
MOD_SUFFIX=".skr2"

cp ${ORIG_PATH}${BASE_FILENAME} ${MOD_PATH}
cp ${MOD_PATH}${BASE_FILENAME}${MOD_SUFFIX} ${ORIG_PATH}${BASE_FILENAME}

echo "BTT SKR2 Board definition applied to Klipper source tree."

exit 0
