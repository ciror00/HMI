import machine
import ujson
import ubinascii
from utils.ntp import timestamp


class DataHandler:
    def __init__(self, model):
        self.uid = ubinascii.hexlify(machine.unique_id())
        self.model = model

    def fill_data(self, measurements):
        result = {}
        result['uid'] = self.uid
        result['model'] = self.model
        result['measures'] = measurements
        result['timestamp'] = timestamp()
        return self.__parse_measurements(result)

    def __parse_measurements(self, measurements):
        return ujson.dumps(measurements)