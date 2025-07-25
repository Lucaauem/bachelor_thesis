from datamodel.soil.Component import Component
from datamodel.soil.SensorReading import SensorReading
from database.db.DBManager import DBManager

class Sensor:
    _component: Component
    _db: DBManager

    def __init__(self, component: Component, db_manager: DBManager) -> None:
        assert component.is_sensor()
        self._component = component
        self._db = db_manager

    def add_measurement(self, reading: SensorReading, value: list) -> None:
        reading.sensor = self._component
        self._db.active_graphdb.add_sensor_reading(reading)
        self._db.active_tsdb.add_measurement(reading.uuid, reading.timestamp, value)
