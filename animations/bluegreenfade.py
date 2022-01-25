from animation import Animation

LED_COUNT = 14 * 3

def main():
    """
    Write a default animation.
    """
    animation = Animation()

    for i in range(255):
        frame = animation.new_frame()
        for led in range(0, LED_COUNT, 3):

            frame[led * 3 + 0] = 0xFF - i  # Blue
            frame[led * 3 + 1] = led*5 # Green
            frame[led * 3 + 2] = 0x00 # Red

            frame[(led + 1) * 3 + 0] = 0xFF - i # Blue
            frame[(led + 1) * 3 + 1] = led*5 # Green
            frame[(led + 1) * 3 + 2] = 0x00 # Red

            frame[(led + 2) * 3 + 0] = 0xFF -i # Blue
            frame[(led + 2) * 3 + 1] = led*5 # Green
            frame[(led + 2) * 3 + 2] = 0x00 # Red

    for i in range(255):
        frame = animation.new_frame()
        for led in range(0, LED_COUNT, 3):

            frame[led * 3 + 0] = i  # Blue
            frame[led * 3 + 1] = led*5 # Green
            frame[led * 3 + 2] = 0x00 # Red

            frame[(led + 1) * 3 + 0] = i # Blue
            frame[(led + 1) * 3 + 1] = led*5 # Green
            frame[(led + 1) * 3 + 2] = 0x00 # Red

            frame[(led + 2) * 3 + 0] = i # Blue
            frame[(led + 2) * 3 + 1] = led*5 # Green
            frame[(led + 2) * 3 + 2] = 0x00 # Red


    with open('bluegreen.bin', 'wb') as output:
            animation.write(output)
    print('Wrote default animation to bluegreen.bin')

if __name__ == '__main__':
    main()
