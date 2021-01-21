import network
import utime


class Wifi:
    def __init__(self, ssid, password=None):
        self.ssid = ssid
        self.password = password
        self.sta_if = None  # Station interface

    def connect(self):
        self.sta_if = network.WLAN(network.STA_IF)
        if not self.sta_if.isconnected():
            self.sta_if.active(True)
            self.sta_if.connect(self.ssid, self.password)
            time_limit = list(utime.localtime())
            time_limit[4] = time_limit[4] + 1  # El indice 4 son los minutos
            while not self.sta_if.isconnected():
                if list(utime.localtime()) > time_limit:
                    self.sta_if.active(False)
                    break
                pass

    def is_connected(self):
        return self.sta_if is not None and self.sta_if.isconnected()
