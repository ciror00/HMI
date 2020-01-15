import network
import machine
import time
#import os

from dataManager import DataManager

class Network:
    def __init__(self, rx, tx):
        self.station = network.WLAN(network.STA_IF)
        self.station.active(True)
        self.serial = machine.UART(2, baudrate=115200, rx=rx, tx=tx, timeout=10)
        self.rx = rx
        self.tx = tx
        self.received = None
        self.networks = []
        self.msj = ""

    def byUART(self):
        self.scanInArray()
        net = self.networks
        n = 0
        #os.system('clear')
        self.serial.write("Available networks.\n\r\n\r")
        for i in net:
            self.serial.write(str(n) + " - " + str(i) + "\n\r")
            n += 1
        self.serial.write("\nSelect the WiFi network:\n\r")
        while True:
            selecting = self.toWrite(False)
            try:
                selecting = int(selecting)
            except:
                selecting = -1
            if selecting < len(self.networks) and selecting >= 0:
                ssid = str(self.networks[selecting])
                self.serial.write("\n\rConnected to the network: " + ssid)
                self.serial.write("\n\rPassword:\n\r")
                passw = self.toWrite(True)
                online = self.connectToWifi(ssid, passw)
                data = DataManager()
                data.save(ssid, passw)
                break
            else:
                self.serial.write("Wrong selection...")
                self.serial.write("\n\rSelect the WiFi network:\n\r")
                selecting = 0

    def scanInArray(self):
        scanning = self.station.scan()
        self.networks.clear()
        for i in scanning:
            self.networks.append(i[0].decode('utf-8'))

    def toWrite(self, secret=False):
        self.received = None
        self.msj = ""
        while True:
            self.received = self.serial.read()
            if self.received != None:
                if self.received == b'\x7f': # Tecla borrar
                    self.serial.write("\r")
                    for _ in range(len(self.msj)):
                        self.serial.write(" ")
                    self.serial.write("\r")
                    self.msj = ""
                    #print(self.msj)
                elif self.received == b'\r': # Tecla enter
                    #print(self.msj)
                    return self.msj
                else:
                    self.msj = self.msj + str(self.received.decode('utf-8'))
                    if not secret:
                        self.serial.write(str(self.received.decode('utf-8')))
                    #print(self.msj)
            else:
                pass

    def connectToWifi(self, ssid, password):
        if not self.station.isconnected():
            self.serial.write("\n\rConnecting to WiFi network...")
            self.station.connect(ssid, password)
            # Wait until connected
            t = time.ticks_ms()
            while not self.station.isconnected():
                if time.ticks_diff(time.ticks_ms(), t) > 10000:
                    self.station.disconnect()
                    self.serial.write("\n\rTimeout. Could not connect.")
                    return False
            self.serial.write("\n\rSuccessfully connected to " + ssid)
            return True
        else:
            self.serial.write("\n\rAlready connected")
            return True