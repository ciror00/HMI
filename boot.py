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
