## Flash RPi MCU

$ sudo systemctl stop klipper.service
$ cd ~/klipper
$ make clean
$ make menuconfig # Choose "Linux Process" and exit saving config
$ make flash
$ sudo systemctl restart klipper_mcu.service
$ sudo systemctl start klipper.service

# verify RPi MCU version number has changed

## Flash Printer

$ sudo systemctl stop klipper.service
$ make clean
$ make menuconfig # set to stm32xx407, serial connection
$ make
$ ~/bin/mod_klipper_src.sh
$ ~/bin/flash_skr2.sh
# there will be a checksum error - ignore
$ ~/bin/restore_klipper_src.sh
# power off printer -- wait for blt led to go out
# power on printer

# verify Printer MCU version number has changed
