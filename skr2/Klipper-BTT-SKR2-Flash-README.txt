[A] BTT SKR2 Upgrade Procedure

The procedure for updating MCU firmware using the SD Card is similar to that of other methods. Instead of using make flash it is necessary to run a helper script, flash-sdcard.sh.

To update a BigTreeTech SKR 2:

Make sure the printer power is ON.

sudo service klipper stop
cd ~/klipper
git pull
make clean
make menuconfig
make

Now copy the modified board_defs.py file from /home/pi:

cp ~/board_defs.py ~/klipper/scripts/spi_flash/board_defs.py

It is up to the user to determine the device location and board name. If a user needs to flash multiple boards, flash-sdcard.sh (or make flash if appropriate) should be run for each board prior to restarting the Klipper service.

Flash the SD Card on the BTT SKR2 board:

~/klipper/scripts/flash-sdcard.sh /dev/ttyAMA0 btt-skr2

There will be a checksum error when finished but you should see the new filename / version in the output.
Turn the printer off, wait maybe 15 seconds and turn it back on.

Verify the printer works.

The klipper instance will be marked as dirty, because the board_defs.py file is different.  ** FIX
In fluidd, you can reset the repo to the current version when checking for updates.

That should be it.  Now for step B.


[B] Building the micro-controller code (for the RPi)

To compile the Klipper micro-controller code, start by configuring it for the "Linux process":

cd ~/klipper/
make menuconfig

In the menu, set "Microcontroller Architecture" to "Linux process", save and exit.

To build and install the new micro-controller code, run:

sudo service klipper stop
make flash
sudo service klipper start

