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
import json

class DBFramework:
    _mqtt_host: str = 'localhost' # TODO Read from file
    _mqtt_port: int = 1884 # TODO Read from file
    _mqtt_clients: MqttClientManager
    _validator: Validator
    _model: Model
    _db_manager: DBManager
    _sensor_manager: SensorManager
    
    def __init__(self) -> None:
        self._mqtt_clients = MqttClientManager()
        self._validator = Validator()
        self._db_manager = DBManager()
        self._sensor_manager = SensorManager()

    def add_mqtt_client(self, id: str) -> None:
        self._mqtt_clients.add_client(id, self._mqtt_host, self._mqtt_port, '#', self.mqtt_received)

    def mqtt_received(self, msg: str) -> None:
        sensor_data = self._sensor_manager.on_new_data(msg)

        if sensor_data is None:
            return
        
        uuid, data = sensor_data
        log(f'Sensor [{uuid}]: New measurement!')

        # Update model
        log(f'Updating model...')
        sensor = self._model.get_object(uuid)
        assert sensor is not None and isinstance(sensor, Component)
        reading = SensorReading(json.dumps(data))
        sensor.add_reading(reading)

        # TODO Validation
        
        log(f'Sensor [{uuid}]: Storing measurement...')
        self._db_manager.active_graphdb.add_sensor_reading(reading)

        log(f'Stored measurement!')

    def set_model(self, model: str) -> None:
        log('Datamodel: Validating...')
        if not self._validator.validate(model, DatasetType.DATAMODEL):
            raise SyntaxError('Datamodel: Not valid!')

        log('Datamodel: Valid!')
        log('Datamodel: Storing in Database...')
        parsed_model = json.loads(model)
        self._model = Model.parse(parsed_model)
        self._db_manager.active_graphdb.insert_model(self._model.serialize())
        log('Datamodel: Stored in Database!')

        log('Sensors: Loading sensors from model...')
        for obj in parsed_model:
            if obj['object_type'] == 'SOIL:COMPONENT' and obj['component_type'] == ComponentType.REAL.name:
                log(f'Sensors: Added "{obj['uuid']}"')
                self._sensor_manager.add_sensor(obj['data'])

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