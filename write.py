#!/usr/bin/env python

from time import sleep

from bltool import connect

LED_COUNT = 14 * 3

def clamp(value):
    return max(0, min(value, 254))

def all_color(ser, red: int, green: int, blue: int):
    red = clamp(red)
    green = clamp(green)
    blue = clamp(blue)
    ser.write(b'\xFF')
    for _ in range(LED_COUNT):
        ser.write(bytes([red, green, blue]))
        sleep(.01)
    ser.write(b'\xFF')

def main():
    with connect() as ser:
        all_color(ser, 0xFE, 0x00, 0x00)
        # while True:
        #     for _ in range(LED_COUNT):
        #         ser.write(b'\xFE\x00\x80')
        #     ser.write(b'\xFF')
        #     sleep(.1)


if __name__ == '__main__':
    main()
