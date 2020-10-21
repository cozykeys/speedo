# CozyKeys Speedo

This repository contains the design files for the CozyKeys Speedo keyboard. The
Speedo is a 66-key ergonomic mechanical keyboard heavily inspired by the
Atreus/Atreus62.

<p align="center">
<img src="http://assets.cozykeys.xyz/images/keyboards/speedo/speedo-v3.0-angle-led-front_800x800.png" alt="Speedo Front"/>
</p>

<p align="center">
<img src="http://assets.cozykeys.xyz/images/keyboards/speedo/speedo-v3.0-angle-led-back_800x800.png" alt="Speedo Back"/>
</p>

## Features

- Powered by an Elite-C microcontroller
- Runs QMK firmware
- Compact ergonomic layout
- Supports underglow via 12 WS2812b RGB LEDs
- Low profile (Switches mounted ~13mm from surface keyboard sits on)
- Case/PCB design files free and open source

## Build Guide

A build guide and parts list are provided at
[./build_guide.md](./build_guide.md).

# Details

## Firmware

The Speedo runs the popular open source QMK firmware:

https://github.com/qmk/qmk_firmware/tree/master/keyboards/speedo

## Default Layout

### Default Layer

<p align="center">
<img src="./layout/speedo_layer_default.svg" alt="Default Layer"/>
</p>

### Function Layer

<p align="center">
<img src="./layout/speedo_layer_fn.svg" alt="Function Layer"/>
</p>

## Case

The case is comprised of 4 layers:

- Top (3mm)
- Switch (4.5mm)
- Middle (4.5mm)
- Bottom (3mm)

### Top

<p align="center">
<img src="./case/speedo_top.svg" alt="Top"/>
</p>

### Switch

<p align="center">
<img src="./case/speedo_switch.svg" alt="Switch"/>
</p>

### Middle

<p align="center">
<img src="./case/speedo_middle.svg" alt="Middle"/>
</p>

### Bottom

<p align="center">
<img src="./case/speedo_bottom.svg" alt="Bottom"/>
</p>

## PCB

<p align="center">
<img src="http://assets.cozykeys.xyz/images/keyboards/speedo/speedo-v3.0-pcb_800x800.png" alt="Speedo PCB"/>
</p>

Artwork provided by [Racknar Teyssier](https://www.instagram.com/artbyrtm/)!

<p align="center">
<img src="https://raw.githubusercontent.com/cozykeys/resources/master/assets/Cozy_Keys_color.svg" alt="PCB Artwork"/>
</p>

## Release Notes

### v3.0

After working on other keyboard projects for quite some time, I revisited the
Speedo with a number of changes:
- Removed the curved thumb key clusters
- Changed the center key layout to add some more space between the left and
  right sides
- Designed a PCB that uses the Elite-C microcontroller with support for 12
  WS2812b RGB LEDs
- Designed a new case to support the updated layout
- Changed versioning scheme to make more sense

### rev2

<p align="center">
<img src="http://assets.cozykeys.xyz/images/keyboards/speedo/speedo-angle_800x800.jpg" alt="Speedo"/>
</p>

The second version fixed the thumb clusters. I had yet to get into PCB design
so this was only ever made via hand-wiring.

### rev1

The first version of the keyboard didn't account for the diameter of standard
keycaps and resulted in a case with faulty thumb

