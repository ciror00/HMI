from utils.mqttHandler import MqttHandler
from utils.httpHandler import HttpHandler


class Sender:
    def __init__(self, wifi, config):
        self._wifi = wifi
        self._active_protocols = config.get_active_protocols()
        # Por ahora quedaria asi con los ifs feitos
        # De esta forma nos ahorramos bastante memoria al no tener que
        # instanciar un protocolo que no se va a usar.
        if 'http' in self._active_protocols:
            self._http = HttpHandler(config.get_http_url(),
                                     config.get_http_token_auth(), config.get_http_endpoint())
        if 'mqtt' in self._active_protocols:
            self._mqtt = MqttHandler(config.get_mqtt_sv(),
                                     config.get_topic_sub(), config.get_topic_pub())
        self._protocol_mapper = {
            'http': self.__post,
            'mqtt': self.__publish
        }

    def __publish(self, obj):
        try_connection(self._wifi)
        # Aca hay que actuaizar el timestamp del envio
        self._mqtt.publish(obj)

    def __post(self, obj):
        try_connection(self._wifi)
        # Aca hay que actuaizar el timestamp del envio
        return self._http.post(obj)

    def send(self, obj_data):
        for protocol in self._active_protocols:
            self._protocol_mapper[protocol](obj_data)


def try_connection(wifi):
    if(not wifi.is_connected()):
        wifi.connect()
        return wifi.is_connected()
    else:
        return True
