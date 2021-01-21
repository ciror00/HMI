import gc
from utils.dataHandler import DataHandler
from utils.sender import Sender
from config.config import Config
from services.measureService import MeasureService
from utils.wifi import Wifi
from utils.ntp import set_time

global RED, GREEN, BLUE
global led

config = Config("config/config.json")
active_sensors = config.get_active_sensors()

wifi = Wifi(config.get_ssid(), config.get_wifi_password())
wifi.connect()

# Se configura la hora desde un servidor NTP
set_time()

measure_service = MeasureService(active_sensors)

# Pasarle a la nueva clase Sender la instancia de wifi para que pueda reconectar
data_handler = DataHandler(config.get_device_model())
sender = Sender(wifi, config)

led.status(1)

while(True):
    measurements = measure_service.measure_active()
    parsed_measurements = data_handler.fill_data(measurements)
    print("\nEnviando data:", parsed_measurements, "\n")
    sender.send(parsed_measurements)
    gc.collect()
    break
