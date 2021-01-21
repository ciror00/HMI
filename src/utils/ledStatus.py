import machine


class Led:
    def __init__(self, red_pin, green_pin, blue_pin):
        self.led = machine.Pin(2, machine.Pin.OUT, value=0)  # led de la ESP32
        # RGB
        self.red = machine.Pin(red_pin, machine.Pin.OUT, value=0)
        self.green = machine.Pin(green_pin, machine.Pin.OUT, value=0)
        self.blue = machine.Pin(blue_pin, machine.Pin.OUT, value=0)
        self.colors = {"RED": [1, 0, 0], "GREEN": [0, 1, 0], "BLUE": [0, 0, 1],
                       "YELLOW": [1, 1, 0], "CYAN": [0, 1, 1], "MAGENTA": [1, 0, 1],
                       "ON": [1, 1, 1], "OFF": [0, 0, 0]}

    def status(self, state=1):
        self.led.value(state)

    def color(self, hue):
        self.red.value(0)
        self.green.value(0)
        self.blue.value(0)
        if hue not in self.colors:
            print("Color does not exist.")
            return
        self.red.value(self.colors[hue][0])
        self.green.value(self.colors[hue][1])
        self.blue.value(self.colors[hue][2])
