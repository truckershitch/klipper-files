# klipper-files

These are just some helper scripts that aid in automatic generation of my basic Klipper configuration files, some basic configuration files, macros, and generally anything I'd like to save for myself in case of data loss, etc.  And if they help anyone else out, that would also be nice.

## Setup

Currently, I have an Ender 3v2 printer, so some of this will be Ender-specific, but maybe not all of it?  At this point, I have a Bondtech DDX / Slice Engineering Copperhead setup and I love it.

See what you can find here in my junkyard.

## Moans and Groans

I had issues when I started with heat creep and had problems fixing it, but the Slice Engineering system is much easier to fix, and parts can be replaced much easier in my opinion. For me, that justifies the cost because I had a few weeks here and there of downtime, some burnt fingers, broken drill bits and small metal rods, etc.  In a twisted way it was fun and I learned a lot.

## Resources


I found a great [DIY Filament Runout Encoder video by Makers Mashup](https://youtu.be/v2mQ4X1J3cs).  It was not hard to build and I've been using it for about six months.  I think it is a simple design and I believe it will be reliable.  And of course DIY is the best.


One dude who really has it together, Bob, the Master of Muppets, has a [good page here](https://projects.ttlexceeded.com/index.html)  And that is no joke.  I modified his start macro for my printer -- it helps get that initial bit of plastic rubbed off the side of the bed so it doesn't drop in the first layer.  I just shifted it to the right side.

<b>You may have to adjust that initial stripe to match your extruder's extrustion limits.</b>  His gcode parameters were a tad too high for my setup.  Klipper threw an error until I tweaked it a little.

## Disclaimer

<b>This is all a work in progress.</b>  So take a look at it but do not take anything as gospel.

I do not claim to be an expert.  In my opinion, when someone says he is, it is a red flag.  To me that means he is not open to change or other opinions, and that is death in science and most pursuits.

If you find a problem with any of this or have a suggestion, do not hesitate to open an issue.  I welcome bug fixes.

[Please do not leave any Watchtower magazines](https://www.youtube.com/watch?v=3YhPZELyF3o)