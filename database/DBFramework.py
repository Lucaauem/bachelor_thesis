from __future__ import annotations
from typing import TYPE_CHECKING
from database.mqtt.ClientManager import ClientManager as MqttClientManager
from database.db.TSDBService import TSDBService
from database.db.GraphDBService import GraphDBService
from database.validation.Validator import Validator
from database.DatasetType import DatasetType
from database.Log import log
import json

if TYPE_CHECKING:
    from typing import Callable

class DBFramework:
    _mqtt_host: str = 'localhost' # TODO Read from file
    _mqtt_port: int = 1884 # TODO Read from file
    _mqtt_clients: MqttClientManager
    _validator: Validator
    _model: list[dict]
    _tsdb: TSDBService
    _graphdb: GraphDBService

    def __init__(self) -> None:
        self._mqtt_clients = MqttClientManager()
        self._validator = Validator()

    def set_tsdb(self, url: str, token: str, org: str) -> None:
        log('TSDB: Connecting...')
        try:
            self._tsdb = TSDBService(url, token, org)
            log('TSDB: Connected successfully!')
        except:
            log('TSDB: Failed to connect!')

    def set_graphdb(self, url: str, user: str, password: str) -> None:
        log('GraphDB: Connecting...')
        try:
            self._graphdb = GraphDBService(url, user, password)
            log('GraphDB: Connected successfully!')
        except:
            log('GraphDB: Failed to connect!')

    def add_mqtt_client(self, id: str, topic: str, on_message: Callable) -> None:
        self._mqtt_clients.add_client(id, self._mqtt_host, self._mqtt_port, topic, on_message)

    def set_model(self, model: str) -> None:
        log('Datamodel: Validating...')
        if not self._validator.validate(model, DatasetType.DATAMODEL):
            raise SyntaxError('Datamodel: Not valid!')

        log('Datamodel: Valid!')
        log('Datamodel: Storing in Database...')
        self._graphdb.insert_model(json.loads(model))
        log('Datamodel: Stored in Database!')

    def launch(self) -> None:
        self._mqtt_clients.start_all()

    def start_client(self, id: str) -> None:
        self._mqtt_clients.start_client(id)

    @property
    def Validator(self) -> Validator:
        return self._validator