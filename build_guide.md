
# Table of Contents

TODO

- [Microcontroller](#microcontroller)
- [Switch Diodes](#switch-diodes)

# Parts List

- Speedo PCB
- Speedo Case
- Elite-C Microcontroller
- Diodes (66)
- Switches (66)
- WS2812b RGB LEDs (12)
- Capacitors (12)
- 6mm M2 Screws (16)
    - https://www.ebay.com/itm/10-50-M2-M6-SS304-Allen-Hex-Hexagon-Socket-Ultra-Thin-Flat-Wafer-Head-Screw-Bolt/153550101060
- 8mm M2 Standoffs (8)

# Tools Required

- 1.5mm Allen Wrench
    - https://www.amazon.com/Wera-05118066001-Screwdriver-Electronic-Applications/dp/B0001P18OQ

# Build Steps

## Firmware

- Flash firmware first in case the MCU is dead

```
git clone https://github.com/qmk/qmk_firmware.git
cd qmk_firmware
python3 -m pip install --user qmk
qmk setup

qmk compile -kb speedo -km default

# On the very first flash or when using the RESET button on the MCU
make speedo:default:dfu

# When flashing via the RESET key on FN layer
TODO
```

## Microcontroller

TODO: Cut legs off of MCU mount

TODO: Solder MCU

## Switch Diodes

- Solder diodes, line side down

## RGB LED Capacitors

- Solder 100nf LED capacitors
    - Polarity doesn't matter

## RGB LEDs

- Solder WS2812b RGB LEDs
    - I lower the soldering iron temp a bit for these, I think I did them at
      340C as opposed to 390C

## Switch Pins

- Solder switches


