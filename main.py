import serial
import time

port = serial.Serial("COM4", 115200, timeout=0, bytesize=8, stopbits=1)

while True:
fichero = open("nombre_del_fichero", "r")
i = 0
for linea in fichero:
    linea = linea.strip()
    port.write(linea+"\r\n")
time.sleep(1)

port.close()