[![Home](https://img.shields.io/badge/Home-red?style=flat)](.)
[![Breadboard](https://img.shields.io/badge/Bread-board-orange?style=flat)](breadboard)
[![Data Analysis](https://img.shields.io/badge/Data-Analysis-yellow?style=flat)](data)

# Firmware

- [Single channel and single thread](https://drive.google.com/file/d/1qZcwXF0fu3xu2bhAN_qnYrPdocArLmrT/view?usp=sharing)

## Flash Firmware to Pi Pico Board

A tact [button] switch connecting pin 30 (RUN) and 28 (Ground) of Pi Pico can be used to reset the board. It can also be used [together] with the [BOOTSEL] button on board to turn the board into a USD drive so that a firmware file (*.uf2) can be dragged and dropped into the drive.

[button]: https://www.amazon.com/dp/B07X8T9D2Q
[together]: https://www.raspberrypi.com/news/how-to-add-a-reset-button-to-your-raspberry-pi-pico
[BOOTSEL]: https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html#resetting-flash-memory

## General Functionalities

### Blink LED on Pi Pico

The LED on board is dedicated to detector 1. In case there is another detector, connect an LED to GPIO PIN 2 to indicate channel 2 trigger.

### Drive an External Buzzer

Since Pi Pico can only output 3.3 V from a GPIO pin, an active [buzzer] that can run at 3 V is needed. Its positive pin should be connected to pin 1 (GP0), and its negative pin should be connected to the ground.

[buzzer]: https://www.amazon.com/dp/B07VRK7ZPF

### Save Data in a Micro SD Card

Micro SD cards instead of USB drives are used to save data from Pi Pico to utilize the on-board [SPI] hardware instead of directly taxing the CPU.

A search of files named `run{nnn}*` in the SD card is made when the Pi Pico is powered/reset. A new file `run{nnn+1}*` is created to avoid overwriting old data. The program stops when 2,000 events are recorded in the file. Push the reset button to start a new run.

The SD card [adapter] requires 3.3 V power supply and should be connected to pin 16 ~ 20 (GP12 ~ 15).

[adapter]: https://www.amazon.com/dp/B0989SM146
[SPI]: https://en.wikipedia.org/wiki/Serial_Peripheral_Interface

### Display Data on an OLED
A 64x128 [OLED] can be connected to Pin 21 and 22 (GP16 and 17) to display run file name and trigger rate.

[OLED]: https://goldenmorninglcd.com/oled-display-module/0.96-inch-128x64-ssd1306-gme12864-11

### Digitize Waveforms from Detector

ADC0 (GP26) is used to digitize the output of detector 1; ADC1 (GP27) is used for detector 2.

### Receive Trigger from Comparator

GP28 is used to receive trigger signals from comparator 1; GP29 is for comparator 2. If the comparator is powered by 3.3 V, the trigger signal is a square pulse of 3.3 V. The width of the pulse is proportional to the width of the signal from the pre-amp. When the voltage received by GP28 or 29 goes above 2 V, the Pi Pico will sound the buzzer, light the LEDs, find the highest sample in the digitized waveforms, and save 64 waveform samples to the SD card.

### Handle High-Rate Data-Taking

By default, the firmware writes to the SD card after 100 events to avoid constant slow IO. If the board loses it power in event 99, all events will be lost.