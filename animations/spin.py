from animation import Animation

LED_COUNT = 14 * 3

def main():
    """
    Write a default animation.
    """
    animation = Animation(LED_COUNT, 1000)

    for i in range(3):
        frame = animation.new_frame()
        for led in range(0, LED_COUNT):

            if (led%3 == i):

                frame[led*3 + 0] = 0xFF  # Blue
                frame[led*3 + 1] = 0xFF # Green
                frame[led*3 + 2] = 0xFF # Red


    with open('spin.bin', 'wb') as output:
            animation.write(output)
    print('Wrote default animation to spin.bin')

if __name__ == '__main__':
    main()
