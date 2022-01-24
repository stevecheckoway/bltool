#!/usr/bin/env python

"""
Programatically create an animation for BlinkyTiles.
"""

from struct import pack

LED_COUNT = 14 * 3

class Animation:
    """
    Simple class to hold an animation for BlinkyTiles.
    """
    def __init__(self, led_count: int = LED_COUNT, speed: int = 10):
        """
        Create a new animation with the given number of LEDs and speed.
        """
        self.led_count = led_count
        self.frames = []
        self.speed = speed
        self.type = 0

    def new_frame(self):
        """
        Append a new frame to the animation and return it. The frame is a bytearray of
        length self.led_count * 3 and the values are BGR, in that order.
        """
        frame = bytearray(self.led_count * 3)
        self.frames.append(frame)
        return frame

    def write(self, output):
        """
        Write the animation to the given output.
        """
        output.write(pack('>IIII', self.led_count, len(self.frames), self.speed, self.type))
        for frame in self.frames:
            output.write(frame)

        animation_size = 16 + len(self.frames) * self.led_count * 3
        remaining = 256 - (animation_size % 256)
        if remaining != 256:
            output.write(bytearray(remaining))

def main():
    """
    Write a default animation.
    """
    animation = Animation()
    for led in range(LED_COUNT):
        frame = animation.new_frame()
        frame[led * 3 + 0] = 0xFF # Red
        frame[led * 3 + 1] = 0x00 # Green
        frame[led * 3 + 2] = 0xFF # Blue
    for led in range(LED_COUNT):
        led = LED_COUNT - led - 1
        frame = animation.new_frame()
        frame[led * 3 + 0] = 0x00 # Red
        frame[led * 3 + 1] = 0xFF # Green
        frame[led * 3 + 2] = 0x00 # Blue
    with open('default-animation.bin', 'wb') as output:
        animation.write(output)
    print('Wrote default animation to default-animation.bin')

if __name__ == '__main__':
    main()
