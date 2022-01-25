from animation import Animation

LED_COUNT = 14 * 3

colors = [[0x00, 0x00, 0xFF], [0x00, 0x33, 0xFF], [0x00, 0x99, 0xFF], [0x00, 0x33, 0xcc],
[0x00, 0xCC, 0xFF], [0x00, 0xFF, 0xFF], [0x33, 0xFF, 0xCC], [0x33, 0xFF, 0x66], [0x33, 0xCC, 0x33],
[0x33, 0xFF, 0xFF], [0xCC, 0xCC, 0XFF],[0xFF, 0x00,0xFF],[0xFF, 0xCC, 0x66],[0xFF, 0x66, 0x00]]

def main():
    """
    Write a default animation.
    """
    animation = Animation(LED_COUNT, 1000)

    for i in range(1):
        frame = animation.new_frame()
        for led in range(0, LED_COUNT, 3):

            frame[led * 3 + 0] = colors[led//3][0]  # Blue
            frame[led * 3 + 1] = colors[led//3][1] # Green
            frame[led * 3 + 2] = colors[led//3][2] # Red

            frame[(led + 1) * 3 + 0] = colors[led//3][0] # Blue
            frame[(led + 1) * 3 + 1] = colors[led//3][1] # Green
            frame[(led + 1) * 3 + 2] = colors[led//3][2] # Red

            frame[(led + 2) * 3 + 0] = colors[led//3][0] # Blue
            frame[(led + 2) * 3 + 1] = colors[led//3][1] # Green
            frame[(led + 2) * 3 + 2] = colors[led//3][2] # Red

    with open('colors.bin', 'wb') as output:
            animation.write(output)
    print('Wrote default animation to colors.bin')

if __name__ == '__main__':
    main()
