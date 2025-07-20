from __future__ import annotations
from typing import TYPE_CHECKING
from database.mqtt.Client import Client as mqttClient

if TYPE_CHECKING:
    from typing import Callable

class ClientManager():
    _clients: dict[str, mqttClient]

    def __init__(self) -> None:
        self._clients = {}

    def add_client(self, id: str, host: str, port: int, topic: str, on_message: Callable) -> None:
        if id in self._clients.keys():
            raise ValueError('MQTT-Client: ID already in use')
        
        client = mqttClient(host, port, topic, on_message)
        self._clients[id] = client

    def start_client(self, id: str) -> None:
        self._clients[id].connect()