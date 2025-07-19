from database.mqtt.ClientManager import ClientManager as MqttClientManager

class DBFramework:
    _mqtt_host: str = 'localhost' # TODO Read from file
    _mqtt_port: int = 1884 # TODO Read from file
    _mqtt_clients: MqttClientManager

    def __init__(self) -> None:
        self._mqtt_clients = MqttClientManager()

    def add_mqtt_client(self, id: str, topic: str) -> None:
        self._mqtt_clients.add_client(id, self._mqtt_host, self._mqtt_port, topic)

    def start_client(self, id: str) -> None:
        self._mqtt_clients.start_client(id)