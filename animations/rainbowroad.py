from animation import Animation

LED_COUNT = 14 * 3
order = [1,2,3,4,5,6,7,9,8,10,11,12,14,13,15,16,18,19,21,20,24,23,22,25,27,26,19,18,17,28,30,31,33,32,35,36,34,30,29,37,38,39,40,41,42]

#color is [r,g,b]
def setColor(frame, led_number, color):
    frame[led_number*3 + 0] = color[2]
    frame[led_number*3 + 1] = color[1]
    frame[led_number*3 + 2] = color[0]

def main():
    """
    Write a default animation.
    """
    animation = Animation(LED_COUNT, 1000)

    for i in range(len(order)):
        frame = animation.new_frame()
        length = len(order)
        length = len(order)
        #red
        setColor(frame, order[i] - 1,[0xFF,0,0])
        #orangex
        setColor(frame, order[(i+1)%length]-1, [0xFF, 0x99, 0x00])
        #yellow
        setColor(frame, order[(i+2)%length]-1, [0xFF, 0xFF, 0x00])
        #Green
        setColor(frame, order[(i+3)%length]-1, [0x00, 0xFF, 0x00])
        #blue
        setColor(frame, order[(i+4)%length]-1, [0x00, 0x00, 0xFF])
        #Violet
        setColor(frame, order[(i+5)%length]-1, [0x66, 0x00, 0xFF])
        #pink
        setColor(frame, order[(i+6)%length]-1, [0xFF, 0x00, 0xFF])

    with open('rainbowroad.bin', 'wb') as output:
            animation.write(output)
    print('Wrote default animation to rainbowroad.bin')

if __name__ == '__main__':
    main()
