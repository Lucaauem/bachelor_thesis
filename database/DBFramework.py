from database.mqtt.ClientManager import ClientManager as MqttClientManager
from database.validation.Validator import Validator
from database.DatasetType import DatasetType
from database.Log import log
from database.db.DBManager import DBManager
from datamodel.soil.ComponentType import ComponentType
from database.sensors.SensorManager import SensorManager
from datamodel.soil.SensorReading import SensorReading
from datamodel.Model import Model
from datamodel.soil.Component import Component
from database.callbacks.CallbackHandler import CallbackHandler
from database.fetching.Fetch import Fetch
from database.callbacks.Events import Events as CallbackEvents
import json

class DBFramework:
    _mqtt_clients: MqttClientManager
    _validator: Validator
    _model: Model
    _db_manager: DBManager
    _sensor_manager: SensorManager
    _callback_handler: CallbackHandler
    _fetch: Fetch
    
    def __init__(self) -> None:
        self._mqtt_clients = MqttClientManager(self._mqtt_received)
        self._validator = Validator(self)
        self._db_manager = DBManager()
        self._sensor_manager = SensorManager(self._db_manager)
        self._callback_handler = CallbackHandler(self)
        self._fetch = Fetch(self)

    def start(self) -> None:
        self._callback_handler.trigger(CallbackEvents.STARTUP)

    def __del__(self):
        self._callback_handler.trigger(CallbackEvents.SHUTDOWN)

    def _mqtt_received(self, msg: str) -> None:
        is_correct, uuid, data = self._sensor_manager.is_correct_reading(msg)

        # Check if reading data is correct
        if not is_correct:
            return
        assert (sensor := self._model.get_object(uuid)) is not None and isinstance(sensor, Component)

        if not self._validator.validate(json.dumps(data), DatasetType.SOIL_DATA):
            log(f'Sensor [{uuid}]: Invalid measurement!')
            return

        # TODO: Move to add_measurement?
        value = data['value']
        del data['value']

        # Update model
        reading = SensorReading(json.dumps(data))
        self._sensor_manager.get_sensor(uuid).add_measurement(reading, value)
        sensor.add_reading(reading)

        log(f'Sensor [{uuid}]: New measurement!')
        self._callback_handler.trigger(CallbackEvents.NEW_SENSOR_READING)

    def update_model(self, model: list[dict]) -> None:
        log('Updating Datamodel...')
        log('Datamodel: Validating...')

        if not self._validator.validate(json.dumps(model), DatasetType.DATAMODEL):
            raise SyntaxError('Datamodel: Not valid!')
        
        log('Datamodel: Parsing...')
        self._model = Model.parse(model)

        log('Datamodel: Storing in Database...')
        self._db_manager.active_graphdb.insert_model(model, self)

        log('Datamodel: Updated!')
        log('Datamodel: Loading sensors...')
        for obj in model:
            if (obj['object_type'] == 'SOIL:COMPONENT') and (obj['component_type'] == ComponentType.REAL.name):
                self._sensor_manager.add_sensor(obj['data'])

        self._callback_handler.trigger(CallbackEvents.MODEL_UPDATE)

    def launch(self) -> None:
        self._mqtt_clients.start_all()

    def clear_model(self) -> None:
        self._db_manager.active_graphdb.clear_model()

    def start_client(self, id: str) -> None:
        self._mqtt_clients.start_client(id)

    @property
    def Validator(self) -> Validator:
        return self._validator
    
    @property
    def DB(self) -> DBManager:
        return self._db_manager
    
    @property
    def Callbacks(self) -> CallbackHandler:
        return self._callback_handler
    
    @property
    def MQTT(self) -> MqttClientManager:
        return self._mqtt_clients
    
    @property
    def Sensors(self) -> SensorManager:
        return self._sensor_manager
    
    @property
    def Fetch(self) -> Fetch:
        return self._fetch
