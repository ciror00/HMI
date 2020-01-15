try:
    import usocket as socket
except:
    import socket
try:
    import ustruct as struct
except:
    import struct

import machine
import utime


class NTP:
    def __init__(self):
        # Se coloca un offset de 70 años (en milisegundos) para convertir a formato Timestamp (GMT -3)
        self.NTP_DELTA = 2208999600 #3155673600
        self.host = "pool.ntp.org"

    def time(self):
        NTP_QUERY = bytearray(48)
        NTP_QUERY[0] = 0x1b
        addr = socket.getaddrinfo(self.host, 123)[0][-1]
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.settimeout(1)
            res = s.sendto(NTP_QUERY, addr)
            msg = s.recv(48)
        finally:
            s.close()
        val = struct.unpack("!I", msg[40:44])[0]
        return val - self.NTP_DELTA

    # Se agrega suma un delta de 30 años al offset para el seteo de fechas en el RTC
    def settime(self):
        t = self.time() - 946684800
        tm = utime.localtime(t)
        machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))

    def timeStamp(self):
        return self.time()