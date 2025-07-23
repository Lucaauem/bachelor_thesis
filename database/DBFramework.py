from __future__ import annotations
from typing import TYPE_CHECKING
from database.mqtt.ClientManager import ClientManager as MqttClientManager
from database.validation.Validator import Validator
from database.DatasetType import DatasetType
from database.Log import log
from database.db.DBManager import DBManager
import json

if TYPE_CHECKING:
    from typing import Callable

class DBFramework:
    _mqtt_host: str = 'localhost' # TODO Read from file
    _mqtt_port: int = 1884 # TODO Read from file
    _mqtt_clients: MqttClientManager
    _validator: Validator
    _model: list[dict]
    _db_manager: DBManager
    
    def __init__(self) -> None:
        self._mqtt_clients = MqttClientManager()
        self._validator = Validator()
        self._db_manager = DBManager()

    def add_mqtt_client(self, id: str, topic: str, on_message: Callable) -> None:
        self._mqtt_clients.add_client(id, self._mqtt_host, self._mqtt_port, topic, on_message)

    def set_model(self, model: str) -> None:
        log('Datamodel: Validating...')
        if not self._validator.validate(model, DatasetType.DATAMODEL):
            raise SyntaxError('Datamodel: Not valid!')

        log('Datamodel: Valid!')
        log('Datamodel: Storing in Database...')
        self._db_manager.active_graphdb.insert_model(json.loads(model))
        log('Datamodel: Stored in Database!')

    def launch(self) -> None:
        self._mqtt_clients.start_all()

    def start_client(self, id: str) -> None:
        self._mqtt_clients.start_client(id)

    @property
    def Validator(self) -> Validator:
        return self._validator
    
    @property
    def DB(self) -> DBManager:
        return self._db_manager