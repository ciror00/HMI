import gc
import machine
import network
import time
import ujson

archivo = open("config.json", "bw")
archivo.write("{}")
archivo.close()
print("Archivo creado")
#with open('config.json') as data:
#    data = ujson.load(data)
#print(data)
#print(data['ssid'])

serial = machine.UART(2, baudrate=115200, rx=16, tx=17, timeout=10)

rcv = None
msj = ""

while True:
    rcv = serial.readline()
    if rcv != None:
        #print(rcv)
        if rcv == b'\x7f': # Tecla borrar
            msj = " "
            print(msj)
        elif rcv == b'\r': # Tecla enter
            break
        else:
            msj = msj + str(rcv.decode('utf-8'))
            print(msj)
    else:
        pass

'''
RED = 'CYS'
PASS = 'Informatica'

station = network.WLAN(network.STA_IF)
station.active(True)

if not station.isconnected():
    print('connecting to network...')
    station.active(True)
    station.connect(RED, PASS)
    while not station.isconnected():
        pass
print('Configuracion de RED:', station.ifconfig())



serial.write("Escaneando redes\n")
redes = station.scan()
for i in redes:
    serial.write(str(i) + ".- " + i[0].decode('utf-8') + "\n")
print('Leyendo puerto')
serial.write("Hello, World!\n")
while True:
    msj = serial.readline()
    if msj != None:
        if msj == b'\r':
            break
        print(msj)
        print(msj.decode('utf-8'))
'''