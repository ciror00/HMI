import ujson


class Config:
    def __init__(self, file_path):
        # *Cargar el archivo json:
        try:
            with open(file_path) as config_file:
                self.config = ujson.load(config_file)
        except OSError as err:
            print("No se puede abrir el archivo de configuracion: {}".format(err))
            # TODO: Cargar configuracion por defecto si el archivo falla

    def get_active_sensors(self):
        sensors_config = self.config["sensors"]
        active_sensors = []
        for sensor, value in sensors_config.items():
            if value:
                active_sensors.append(sensor)
        return active_sensors

    def get_active_protocols(self):
        protocols_config = self.config["protocols"]
        active_protocols = []
        for protocol, obj in protocols_config.items():
            if obj["state"]:
                active_protocols.append(protocol)
        return active_protocols

    def get_mqtt_sv(self):
        return self.config["protocols"]["mqtt"]["sv"]

    def get_topic_sub(self):
        return self.config["protocols"]["mqtt"]["topic_sub"]

    def get_topic_pub(self):
        return self.config["protocols"]["mqtt"]["topic_pub"]

    def get_http_url(self):
        return self.config["protocols"]["http"]["base_url"]

    def get_http_endpoint(self):
        return self.config["protocols"]["http"]["endPoint"]

    def get_http_token_auth(self):
        return self.config["protocols"]["http"]["token_auth"]

    def get_interval(self):
        return self.config["parameters"]["interval"]

    def get_ssid(self):
        return self.config["network"]["ssid"]

    def get_wifi_password(self):
        return self.config["network"]["password"]

    def get_device_model(self):
        return self.config["model"]
