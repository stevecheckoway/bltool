#!/usr/bin/env python3

"""
Example script file creation.

Format is a sequence of two 32-bit, big-endian integers:

  [animation, loop_count].

The first integer, animation, is the 0-based animation index of the animations
in flash. This is not the sector number so that the sectors can change as long
as files are in the same order.

At the end of the script, it loops back to the beginning.

An animation number of 0xFFFFFFFF loops back to the beginning. An animation
number of 0xFFFFFFF0 selects a random animation.

A loop_count of 0xFFFFFFFF indicates playing the animation forever.
"""

from struct import pack

RANDOM = 0xFFFFFFF0

def main():
    data = bytearray()
    data.extend(pack('>II', 0, 1)) # Animation 0, 1 time
    data.extend(pack('>II', 1, 1)) # Animation 1, 1 time
    data.extend(pack('>II', 2, 1))
    data.extend(pack('>II', 3, 1))
    data.extend(pack('>II', 4, 2))
    data.extend(pack('>II', 3, 1))
    data.extend(pack('>II', 2, 1))
    data.extend(pack('>II', 1, 1)) # Animation 1, 1 time
    with open('0-4.script', 'wb') as output:
        output.write(data)
    
    with open('random.script', 'wb') as output:
        output.write(pack('>II', RANDOM, 2)) # Random animation, 2 times

if __name__ == '__main__':
    main()
