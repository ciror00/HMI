import machine

class Led:
    def __init__(self):
        self.led = machine.Pin(2, machine.Pin.OUT, value=0)
        # Leds RGB
        self.blue = machine.Pin(19, machine.Pin.OUT, value=0) # blue
        self.green = machine.Pin(18, machine.Pin.OUT, value=0) # green
        self.red = machine.Pin(15, machine.Pin.OUT, value=0) # red
        self.colors = {"BLUE": [1,0,0], "GREEN": [0,1,0], "RED": [0,0,1], 
            "CIAN": [1,1,0], "YELLOW": [0,1,1], "MAGENTA": [1,0,1], "WHITE": [1,1,1], "BLACK": [0,0,0]}

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