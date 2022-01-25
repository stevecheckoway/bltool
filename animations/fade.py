from animation import Animation

LED_COUNT = 14 * 3

def main():
    """
    Write a default animation.
    """
    animation = Animation(LED_COUNT, 1000)

    for i in range(6):
        frame = animation.new_frame()
        for led in range(0, LED_COUNT):

            frame[led * 3 + 0] = 0xFF - i*led  # Blue
            frame[led * 3 + 1] = 0xFF # Green
            frame[led * 3 + 2] = 0xFF - i*led # Red

    for i in range(6):
        frame = animation.new_frame()
        for led in range(0, LED_COUNT):

            frame[led * 3 + 0] = 0xFF - 6*led   # Blue
            frame[led * 3 + 1] = 0xFF - i*(LED_COUNT - led)
            frame[led * 3 + 2] = 0xFF - 6*led # Red

    for i in range(6):
        frame = animation.new_frame()
        for led in range(0, LED_COUNT):

            frame[led * 3 + 0] = 0xFF - 6*led  # Blue
            frame[led * 3 + 1] = max(0xFF - 6*(LED_COUNT - led) - i*LED_COUNT, 0)
            frame[led * 3 + 2] = max(0xFF - 6*led - i*LED_COUNT, 0) # Red

    for i in range(6):
        frame = animation.new_frame()
        for led in range(0, LED_COUNT):

            frame[led * 3 + 0] = 0xFF - 6*led + i*led # Blue
            frame[led * 3 + 1] = max(0xFF - 6*(LED_COUNT - led) - 6*LED_COUNT, 0) + i*led #greem
            frame[led * 3 + 2] = max(0xFF - 6*led - 6*LED_COUNT, 0) + i*led # Red


    with open('fade.bin', 'wb') as output:
            animation.write(output)
    print('Wrote default animation to fade.bin')

if __name__ == '__main__':
    main()
