import usocket as socket
import ustruct as struct
import utime
from machine import RTC

# Se coloca un offset de 70 años (en milisegundos) para convertir a formato Timestamp (GMT -3)
NTP_DELTA = 2208999600  # DELTA Legacy: 3155673600
DELTA_OFFSET = 946739082
HOST = "pool.ntp.org"


def __time():
    ntp_query = bytearray(48)
    ntp_query[0] = 0x1b
    addr = socket.getaddrinfo(HOST, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        s.sendto(ntp_query, addr)
        msg = s.recv(48)
    finally:
        s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    return val - NTP_DELTA


def set_time():
    t = __time() - 946684800  # delta de 30 años al offset para el seteo de fechas en el RTC
    tm = utime.localtime(t)
    RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))


def timestamp():
    t = RTC().datetime()
    unixtime = utime.mktime(t)
    return unixtime + DELTA_OFFSET


def human_date():
    return RTC().datetime()
