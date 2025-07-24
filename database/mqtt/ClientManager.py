from __future__ import annotations
from typing import TYPE_CHECKING
from database.mqtt.Client import Client as mqttClient
import toml

if TYPE_CHECKING:
    from typing import Callable

class ClientManager():
    _DEFAULT_TOPIC = '#'

    _clients: dict[str, mqttClient]
    _callback: Callable

    def __init__(self, callback: Callable) -> None:
        self._clients = {}
        self._callback = callback

    def add_client(self, toml_path: str) -> str:
        with open(toml_path) as f:
            file = toml.load(f)
        
        id = f'MQTT_{len(self._clients.keys())}'
        
        client = mqttClient(id, file['host'], file['port'], self._DEFAULT_TOPIC, self._callback)
        self._clients[id] = client

        return id

    def start_client(self, id: str) -> None:
        self._clients[id].connect()

    def start_all(self) -> None:
        for client in self._clients.keys():
            self._clients[client].connect()
