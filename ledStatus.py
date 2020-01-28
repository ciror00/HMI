import machine

class Led:
    def __init__(self, bluePin, greenPin, redPin):
        self.led = machine.Pin(2, machine.Pin.OUT, value=0)
        # Leds RGB
        self.blue = machine.Pin(bluePin, machine.Pin.OUT, value=0) # blue
        self.green = machine.Pin(greenPin, machine.Pin.OUT, value=0) # green
        self.red = machine.Pin(redPin, machine.Pin.OUT, value=0) # red
        self.colors = {"BLUE": [1,0,0], "GREEN": [0,1,0], "RED": [0,0,1], 
            "CYAN": [1,1,0], "YELLOW": [0,1,1], "MAGENTA": [1,0,1], "ON": [1,1,1], "OFF": [0,0,0]}

    def status(self, state):
        self.led.value(state)

    def color(self, hue):
        self.blue.value(0)
        self.green.value(0)
        self.red.value(0)
        try:
            self.blue.value(self.colors[hue][0])
            self.green.value(self.colors[hue][1])
            self.red.value(self.colors[hue][2])
        except:
            print("Color does not exist.")