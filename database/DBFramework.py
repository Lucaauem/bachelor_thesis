from __future__ import annotations
from typing import TYPE_CHECKING
from database.mqtt.ClientManager import ClientManager as MqttClientManager
from database.validation.Validator import Validator
from database.DatasetType import DatasetType

if TYPE_CHECKING:
    from typing import Callable

class DBFramework:
    _mqtt_host: str = 'localhost' # TODO Read from file
    _mqtt_port: int = 1884 # TODO Read from file
    _mqtt_clients: MqttClientManager
    _validator: Validator

    def __init__(self) -> None:
        self._mqtt_clients = MqttClientManager()
        self._validator = Validator()

    def add_mqtt_client(self, id: str, topic: str, on_message: Callable) -> None:
        self._mqtt_clients.add_client(id, self._mqtt_host, self._mqtt_port, topic, on_message)

    def start_client(self, id: str) -> None:
        self._mqtt_clients.start_client(id)

    # TODO: Private
    def validate(self, data: str, type: DatasetType) -> None:
        print(self._validator.validate(data, type))