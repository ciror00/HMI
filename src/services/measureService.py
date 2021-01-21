from machine import Pin, ADC, I2C
from libs.bmp280 import BMP280
from libs.adxl345 import ADXL345
from utils.constants import Const
from utils.ntp import timestamp
from utils.logger import logger


class MeasureService:

    def __init__(self, active_sensors):
        self.active_sensors = active_sensors
        self.sensor_mapper = {}
        i2c = I2C(sda=Pin(Const._SDA), scl=Pin(Const._SCL))

        # Es posible que estos booleanos sean de utilidad en un futuro
        # para no tener que re-preguntar cuales sensores estan activos.
        # Por el momento son locales a __init__
        is_enabled_light_sensor = Const._LIGHT in self.active_sensors
        is_enabled_environmental_sensor = Const._TEMPERATURE in self.active_sensors or Const._PRESSURE in self.active_sensors or Const._ALTITUDE in self.active_sensors
        is_enabled_accel_rotation_sensor = Const._ACCELEROMETER in self.active_sensors or Const._ROTATION in self.active_sensors

        if is_enabled_light_sensor: self._init_light_sensor()
        if is_enabled_environmental_sensor: self._init_environmental_sensor(i2c)
        if is_enabled_accel_rotation_sensor: self._init_accel_rotation_sensor(i2c)

    def __temperature(self):  # *Temperatura medida en Celcius [C]
        temp = None
        try:
            temp = self.bmp280.temperature
        except Exception as err:
            self.active_sensors.remove(Const._TEMPERATURE)
            logger("[ERROR] Sensor de temperatura dejo de funcionar: {}".format(err), "error")
        return temp

    def __pressure(self):  # *Presión medido en Pascales [Pa]
        press = None
        try:
            press = self.bmp280.pressure/100
        except Exception as err:
            self.active_sensors.remove(Const._PRESSURE)
            logger("[ERROR] Sensor de presión dejo de funcionar: {}".format(err), "error")
        return press

    def __light(self):  # *Luz medida en Lumens [Lm]
        light = None
        try:
            light = (self.light_pin.read()*Const._ANALOG_PERCENT)/Const._LIGHT_THRESHOLD
        except Exception as err:
            self.active_sensors.remove(Const._LIGHT)
            logger("[ERROR] Sensor de luz dejo de funcionar: {}".format(err), "error")
        return light

    def __altitude(self):  # *Altitud medida en [M] Basado en la libería BMP180
        altitude = None
        try:
            altitude = round(44330*(1-pow((self.__pressure())/abs(Const._SEA_LEVEL), 0.1903)), 2)
        except Exception as err:
            self.active_sensors.remove(Const._ALTITUDE)
            logger("[ERROR] Sensor de altitud dejo de funcionar: {}".format(err), "error")
        return altitude

    def __accelerometer(self):  # *Referencia del giroscopo como señal analógica
        accel = tuple()
        try:
            accel = (self.adxl345.xValue, self.adxl345.yValue, self.adxl345.zValue)
        except Exception as err:
            self.active_sensors.remove(Const._ACCELEROMETER)
            logger("[ERROR] Sensor de aceleración dejo de funcionar: {}".format(err), "error")
        return accel

    def __rotation(self):  # *Ángulos según la posicion media del sensor: Alabeo y Cabeceo
        rotation = None
        try:
            rotation = self.adxl345.RP_calculate(
                self.adxl345.xValue,
                self.adxl345.yValue,
                self.adxl345.zValue)
        except Exception as err:
            self.active_sensors.remove(Const._ROTATION)
            logger("[ERROR] Sensor de rotación dejo de funcionar: {}".format(err), "error")
        return rotation

    def measure_active(self):
        measurements = []

        for sensor in self.active_sensors:
            measurements.append({"sensor": sensor, "data": self.sensor_mapper[sensor](),
                                 "timestamp": timestamp()})
        return measurements

    def _init_light_sensor(self):
        try:
            self.light_pin = ADC(Pin(Const._LIGHT_PIN))
            self.sensor_mapper[Const._LIGHT] = self.__light
        except Exception as err:
            self.active_sensors.remove(Const._LIGHT)
            logger("[ERROR] Sensor ADC no pudo ser instanciado: {}".format(err), "error")

    def _init_environmental_sensor(self, i2c):
        try:
            self.bmp280 = BMP280(i2c)
            self.sensor_mapper[Const._TEMPERATURE] = self.__temperature
            self.sensor_mapper[Const._PRESSURE] = self.__pressure
            self.sensor_mapper[Const._ALTITUDE] = self.__altitude
        except Exception as err:
            if Const._TEMPERATURE in self.active_sensors:
                self.active_sensors.remove(Const._TEMPERATURE)
            if Const._PRESSURE in self.active_sensors:
                self.active_sensors.remove(Const._PRESSURE)
            if Const._ALTITUDE in self.active_sensors:
                self.active_sensors.remove(Const._ALTITUDE)
            logger("[ERROR] Sensor BMP280 no pudo ser instanciado: {}".format(err), "error")

    def _init_accel_rotation_sensor(self, i2c):
        try:
            self.adxl345 = ADXL345(i2c)
            self.sensor_mapper[Const._ACCELEROMETER] = self.__accelerometer
            self.sensor_mapper[Const._ROTATION] = self.__rotation
        except Exception as err:
            if Const._ACCELEROMETER in self.active_sensors:
                self.active_sensors.remove(Const._ACCELEROMETER)
            if Const._ROTATION in self.active_sensors:
                self.active_sensors.remove(Const._ROTATION)
            logger("[ERROR] Sensor ADXL345 no pudo ser instanciado: {}".format(err), "error")
