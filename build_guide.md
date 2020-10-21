# Table of Contents

- [Parts List](#parts-list)
- [Build Steps](#build-steps)
    - [Firmware](#firmware)
    - [Microcontroller](#microcontroller)
    - [Switch Diodes](#switch-diodes)
    - [RGB LED Capacitors](#rgb-led-capacitors)
    - [RGB LEDs](#rgb-leds)
    - [Switches](#switches)
    - [Case Bottom](#case)
    - [Testing](#testing)
    - [Case Top](#case)
- [All Done](#all-done)

# Parts List

- Speedo PCB
    - Not available for sale yet so you'll need to get it manufactured online -- I use [PCBWay](https://www.pcbway.com/)
    - Gerber files are available in the [v3.0 release folder](./releases/v3.0/)
- Speedo Case
    - Not available for sale yet so you'll need to get it manufactured online -- I use [Ponoko](https://www.ponoko.com)
    - Case files are available in the [v3.0 release folder](./releases/v3.0/)
    - Top and bottom layers should be 3.0mm thick
    - Middle and switch layers should be 4.5mm thick
- Elite-C Microcontroller
    - Available in various stores such as [Keebio](https://keeb.io/products/elite-c-low-profile-version-usb-c-pro-micro-replacement-atmega32u4)
- 66 x SMD 1N4148 Diodes
    - https://www.digikey.com/en/products/detail/taiwan-semiconductor-corporation/1N4148W-RHG/7357066
    - Note: The v3.0 PCB **only supports SMD diodes**; I plan to update the footprints in v3.1 to allow either SMD or through hole
- 66 x Switches
    - PCB or plate mount are both supported
    - Only MX-style switches will work; choc low profile, matias, etc will not
    - If using a 4.5mm plate, plate mount will be "friction fit" meaning that they won't clip onto the plate
    - This is perfectly fine as demonstrated in this build guide
- 12 x WS2812b RGB LEDs (Optional)
    - https://www.digikey.com/en/products/detail/adafruit-industries-llc/1655/5154679
- 12 x 100nf Capacitors (Optional)
    - Recommended if adding the RGB LEDs
    - https://www.digikey.com/en/products/detail/kemet/C0805C104K5RACTU/411445
- 16 x 6mm M2 Screws
    - https://www.ebay.com/itm/10-50-M2-M6-SS304-Allen-Hex-Hexagon-Socket-Ultra-Thin-Flat-Wafer-Head-Screw-Bolt/153550101060
- 8 x 8mm M2 Standoffs
    - https://www.ebay.com/itm/New-highest-quality-2mm-Brass-Standoff-Spacer-M2-Female-x-M2-Female-Freeshipping/182032208680

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-1-parts_1600x1600.png" alt="parts" width="480" height="480"/>
</p>

# Build Steps

## Firmware

It's always a good idea to flash the firmware first in case the MCU is dead. The firmware and instructions are available in the QMK repository:

https://github.com/cozykeys/qmk_firmware/tree/speedo/keyboards/speedo

## Microcontroller

The Elite-C should be placed on the top side of the PCB such that the side with
the electronic components is facing down. The pin headers should have the
longer legs facing up.

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-2-mcu-placement_1600x1600.png" alt="mcu-placement" width="480" height="480"/>
</p>

The long legs of the pin header will need to be clipped to fit within the case.
I've found the easiest way to do this is to place a piece of tape on top of the
Elite-C to hold the legs as they are clipped, otherwise they can fly off and
potentially be dangerous.

It can actually hurt a bit to hold the tape directly due to how thick the pins
are and the force when they are clipped so I also like to place a piece of foam
on top. Anything soft and relatively thick (Like a sock) would probably work.

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-3-mcu-trimming-1_1600x1600.png" alt="mcu-trimming-1" width="480" height="480"/>
</p>

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-4-mcu-trimming-2_1600x1600.png" alt="mcu-trimming-2" width="480" height="480"/>
</p>

The end result is that the top side of the Elite-C should be quite flat. This ensures there is plenty of clearance in the case.

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-5-mcu-trimmed_1600x1600.png" alt="mcu-trimmed" width="480" height="480"/>
</p>

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-6-mcu-profile_1600x1600.png" alt="mcu-profile" width="480" height="480"/>
</p>

An unintended benefit is that this actually makes the pins easier to solder as well.

Solder the first and last pin on each of the pin headers so that they are held
in place and make sure that the pin headers are sitting flush against the
Elite-C.

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-7-mcu-corners_1600x1600.png" alt="mcu-corners" width="480" height="480"/>
</p>

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-8-mcu-legs_1600x1600.png" alt="mcu-legs" width="480" height="480"/>
</p>

If everything looks good, solder the rest of the pins.

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-9-mcu-soldered_1600x1600.png" alt="mcu-soldered" width="480" height="480"/>
</p>

With all of the pins on the Elite-C soldered, make sure it is seated on the top
side of the PCB. The top side of the PCB is the side without all of the artwork.

Tape the Elite-C down so that it will remain in place while soldering it to the
PCB.

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-10-mcu-taped_1600x1600.png" alt="mcu-taped" width="480" height="480"/>
</p>

Solder the pins; I like to start with the ends of each pin header first to
guarantee it stays in place.

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-11-mcu-finished_1600x1600.png" alt="mcu-finished" width="480" height="480"/>
</p>

The end result will look as follows.

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-12-mcu-finished-bottom_1600x1600.png" alt="mcu-finished-bottom" width="480" height="480"/>
</p>

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-13-mcu-finished-top_1600x1600.png" alt="mcu-finished-top" width="480" height="480"/>
</p>

## Switch Diodes

The v3.0 PCB only supports SMD diodes which can be intimidating at first but
with a bit of practice they are actually quite easy to solder, even by hand.

I will assume that if you intend to use solder paste and a rework station you
are familiar with how to do so.

To solder the diodes by hand, start by flowing a small dab of solder onto one
pad by touching the iron to the pad and very briefly applying the solder.

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-14-diode-start_1600x1600.png" alt="diode-start" width="480" height="480"/>
</p>

Using tweezers, hold the diode in one hand and the soldering iron in the other.
Touch the iron to the pad with the solder already applied and move the diode
into place with the opposite hand, making sure that it lines up correctly.

Note that **polarity is important**; ensure that the direction of the diode is
correct. All of the diodes should have the side with the line facing down. The
silk screen also indicates which side the line should be on.

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-15-diode-mount-1_1600x1600.png" alt="diode-mount-1" width="480" height="480"/>
</p>

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-16-diode-mount-2_1600x1600.png" alt="diode-mount-2" width="480" height="480"/>
</p>

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-17-diode-mount-3_1600x1600.png" alt="diode-mount-3" width="480" height="480"/>
</p>

With the diode in place, the second pad can be soldered as normal with solder
wire.

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-18-diode-complete_1600x1600.png" alt="diode-complete" width="480" height="480"/>
</p>

To speed up the build process I like to do the diodes in a sort of assembly
line where I do each of the previous steps for every diode before moving on to
the next step.

So first I dab the solder onto one pad for each diode.

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-19-diodes-started_1600x1600.png" alt="diodes-started" width="480" height="480"/>
</p>

Next I place each diode but leave the second pad unfinished.

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-20-dioes-mounted_1600x1600.png" alt="dioes-mounted" width="480" height="480"/>
</p>

Finally I go through and solder the second pad on each.

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-21-diodes-completed_1600x1600.png" alt="diodes-completed" width="480" height="480"/>
</p>

## RGB LED Capacitors

If you plan on adding the WS2812b RGB LEDs, I recommend also adding a
100nf decoupling capacitor next to each one.

If you look at any off-the-shelf strip, you will see that they also have these.
As for why, I'll leave that as an exercise for the reader:

https://en.wikipedia.org/wiki/Decoupling_capacitor

These can also be intimidating due to how small they are but again, they're
actually quite easier to solder.

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-22-capacitor_1600x1600.png" alt="capacitor" width="480" height="480"/>
</p>

Follow the exact same technique used for the diodes, applying solder to one pad
first.

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-23-capacitor-start_1600x1600.png" alt="capacitor-start" width="480" height="480"/>
</p>

Polarity **does not matter** on the capacitors so don't worry about which way
it's facing.

Heat the pad while positioning the capacitor. Once it's in place, solder the
other end.

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-24-capacitor-complete_1600x1600.png" alt="capacitor-complete" width="480" height="480"/>
</p>

## RGB LEDs

The WS2812b RGB LEDs can be quite frustrating to solder by hand so my best
advice for this portion is to be patient and don't fret if things don't work on
the first try.

The orientation of the LEDs is very important. One corner will have a notch in
it and the silk screen on the PCB indicates where this corner should go via an
L shape next to the corresponding pad.

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-25-led_1600x1600.png" alt="led" width="480" height="480"/>
</p>

The artwork covers the silk screen on a couple of the LEDs but just follow the
orientation of the previous/next LEDs in sequence. The sequence should be
obvious from the silk screened IDs (L1, L2, etc.).

The approach for soldering the LEDs is similar to the diodes and capacitors.
Begin by applying a dab of solder to just one of the pads, then place the
component while heating that pad, and finally complete the remaining pads.

One thing that makes these more frustrating to solder is that the legs are
under the component and raise it up off of the PCB slightly. While placing it,
I recommend pressing down slightly to ensure it sits as flush as possible with
the PCB.

Also, these LEDs are fairly easy to burn out so try not to hold the iron to a
pad for too long. Instead, touch the iron to the pad and apply the solder wire
briefly.  If it doesn't flow correctly, simply pull the iron/wire back, give it
time to cool, and try again.

The final result will look as follows.

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-26-led-complete-1_1600x1600.png" alt="led-complete-1" width="480" height="480"/>
</p>

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-27-led-complete-2_1600x1600.png" alt="led-complete-2" width="480" height="480"/>
</p>

## Switches

The switches are the most straight forward part of the build process. Simply
place them in an order that makes sense and solder the two through-hole pins.

In my case, I'm using Kailh silent box pink switches which are plate mount.
Plate mount have the potential to be slightly crooked due to not having the two
extra legs so I will be attaching them one column at a time starting from each
end.

In a previous build I used PCB mount switches and in that case I started with
just the four corners first. The important thing is just to make sure the
switch is seated all the way into the plate and the PCB.

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-28-switches-start_1600x1600.png" alt="switches-start" width="480" height="480"/>
</p>

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-29-switches-start-2_1600x1600.png" alt="switches-start-2" width="480" height="480"/>
</p>

As mentioned, if using plate mount switches, it's a good idea to double check
that they are aligned.

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-30-switches-align_1600x1600.png" alt="switches-align" width="480" height="480"/>
</p>

Repeat until all switches are soldered.

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-31-switches-soldered-1_1600x1600.png" alt="switches-soldered-1" width="480" height="480"/>
</p>

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-32-switches-soldered-2_1600x1600.png" alt="switches-soldered-2" width="480" height="480"/>
</p>

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-33-switches-complete_1600x1600.png" alt="switches-complete" width="480" height="480"/>
</p>

## Case Bottom

The case is comprised of four layers of acrylic plastic that total 15mm in
height (3.0 + 4.5 + 4.5 + 3.0).

There are 8 x 8mm brass standoffs in the middle and then two 6mm screws for
each that screw in from the top and bottom.

Get the hardware ready to put together the case. For this portion, you'll need
all 8 standoffs but just 8 of the screws.

Optionally, you can try to use a threadlocker like Loctite; however, use this
at your own risk. These might have the potential to expand which could crack
the acrylic.

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-34-case-hardware_1600x1600.png" alt="case-hardware" width="480" height="480"/>
</p>

Before putting any screws in the case, **make sure it's oriented correctly**.
The access hole for the reset switch is not exactly in the center of the case.

If the sheet of acrylic is flat and the screws are being dropped into the holes
from the top, the access hole should be to the right, not the left. It's not
the end of the world if you screw this up. The reset switch can still be easily
pressed with a bent paper clip.

If using a threadlocker, apply it to the screw.

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-35-screw-loctite_1600x1600.png" alt="screw-loctite" width="480" height="480"/>
</p>

Drop the screw through the hole, then hold the standoff with plyers or similar
and fasten the screw.

**Do not overtighten the screw.** Acrylic is brittle and will crack easily; I
made this mistake on my build. For this reason I'd recommend only hand
tightening the screws and not using something like an electric screwdriver.

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-36-screw_1600x1600.png" alt="screw" width="480" height="480"/>
</p>

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-37-case-cracking_1600x1600.png" alt="case-cracking" width="480" height="480"/>
</p>

With all of the standoffs in place, place the middle case layer on top of the
bottom layer and then the switch layer on top of that. I recommend not
attaching the top of the case until after testing.

## Testing

Plug the keyboard in and if you haven't yet flashed the firmware, do so now.

Test that all the keys are working. I generally use:

https://www.keyboardtester.com/

Test that the RGBs are working. Cycle through the RGB modes and make sure that
they look correct. On my first build, I had to fix one of the solder joints
which is why I now leave the case open until it's all tested.

Fortunately, given that the RGBs are in sequence it's usually easy to tell
where the problem is if there is one.

For example, if the first four LEDs look correct but the rest flicker, one or
more solder joints on the fifth LED probably needs to be fixed.

Similarly, if one doesn't light up, it's possible the power pin on that LED is
not properly soldered.

## Case Top

With the keyboard tested, it's time to close up.

Grab the remaining eight screws and fasten the top layer down.

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-38-hand-screwing_1600x1600.png" alt="hand-screwing" width="480" height="480"/>
</p>

Alas! A keyboard!

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-39-hardware-complete_1600x1600.png" alt="hardware-complete" width="480" height="480"/>
</p>

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-40-without-keycaps_1600x1600.png" alt="without-keycaps" width="480" height="480"/>
</p>

All that's left is to put some keycaps on it and choose a cable.

## All Done

Don't forget to take some pictures for internet points.

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-41-complete-rgb-angle_1600x1600.png" alt="complete-rgb-angle" width="480" height="480"/>
</p>

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-42-complete-rgb-straight_1600x1600.png" alt="complete-rgb-straight" width="480" height="480"/>
</p>

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-43-complete-straight_1600x1600.png" alt="complete-straight" width="480" height="480"/>
</p>

<p align="center">
<img src="http://assets.cozykeys.xyz/images/builds/speedo-v3.0-2/speedo-v3.0-b2-44-complete-rgb-straight-light_1600x1600.png" alt="complete-rgb-straight-light" width="480" height="480"/>
</p>
