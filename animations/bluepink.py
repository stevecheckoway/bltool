from animation import Animation

LED_COUNT = 14 * 3

def main():
    """
    Write a default animation.
    """
    animation = Animation(LED_COUNT, 100)

    for i in range(3):
        frame = animation.new_frame()
        for led in range(0, LED_COUNT):
            frame[led * 3 + 0] = 0xFF - led*5  # Blue
            frame[led * 3 + 1] = 0x00 # Green
            frame[led * 3 + 2] = led*5 # Red

            #if led == i:
            #    frame[led * 3 + 1] = 0xFF

    with open('bluepink.bin', 'wb') as output:
            animation.write(output)
    print('Wrote default animation to bluepink.bin')

if __name__ == '__main__':
    main()
