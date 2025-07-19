from database.mqtt.Client import Client as mqttClient

class ClientManager():
    _clients: dict[str, mqttClient]

    def __init__(self) -> None:
        self._clients = {}

    def add_client(self, id: str, host: str, port: int, topic: str) -> None:
        client = mqttClient(host, port, topic)

        self._clients[id] = client

    def start_client(self, id: str) -> None:
        self._clients[id].connect()