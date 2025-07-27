from __future__ import annotations
from typing import TYPE_CHECKING
from py2neo import Graph, Node, Relationship, NodeMatcher
from database.Log import log
import json

if TYPE_CHECKING:
    from datamodel.soil.SensorReading import SensorReading
    from database.DBFramework import DBFramework

class GraphDBService:
    _graph: Graph | None = None
    _uri: str
    _auth: tuple[str, str]

    def __init__(self, uri: str, user: str, password: str) -> None:
        self._uri = uri
        self._auth = (user, password)

    def connect(self) -> None:
        assert self._graph is None
        self._graph = Graph(self._uri, auth=self._auth)

    def disconnect(self) -> None:
        assert self._graph is not None
        self._graph = None

    def clear_model(self) -> None:
        assert self._graph is not None
        self._graph.run('MATCH (n) DETACH DELETE n')
        
    def insert_model(self, model: list[dict], fw: DBFramework) -> None:
        assert self._graph is not None
        
        for obj in model:
            self._insert_object(obj, fw)

        for obj in model:
            self._create_relation(obj, model)

    def add_sensor_reading(self, reading: SensorReading) -> None:
        assert self._graph is not None

        node_data = {
            'id' : reading.id,
            'data' : json.dumps(reading.serialize())
        }

        sensor_node = self._graph.nodes.match('SOIL:COMPONENT', id=reading.sensor.uuid).first()
        reading_node = Node('SOIL:SENSOR_READING', **node_data)
        self._graph.merge(reading_node, 'SOIL:SENSOR_READING', 'id')

        rel = Relationship(sensor_node, 'MEASURED', reading_node)
        self._graph.merge(rel)

    def _insert_object(self, obj: dict, fw: DBFramework) -> None:
        assert self._graph is not None
        obj_type = obj['object_type']

        if obj['object_type'] == 'SOIL:SENSOR_READING':
            value = obj['data']['values']
            del obj['data']['values']
            fw.DB.active_tsdb.add_measurement(obj['uuid'], obj['data']['timestamp'], value)

        properties = {
            'id': obj['uuid'] if obj['object_type'] != 'SOIL:SENSOR_READING' else obj['mea_id'],
            'data': json.dumps(obj)
        }

        node = Node(obj_type, **properties)
        self._graph.merge(node, obj_type, 'id')

    def _create_relation(self, obj, model) -> None:
        assert self._graph is not None

        if obj['object_type'] != 'SOIL:SENSOR_READING':
            for key in obj['references']:
                for target in obj['references'][key]:
                    from_node = self._graph.nodes.match(obj['object_type'], id=obj['uuid']).first()
                    to_node = self._graph.nodes.match(GraphDBService._get_label(target, model), id=target).first()

                    rel = Relationship(from_node, key, to_node)
                    self._graph.merge(rel)
        else:
            target = obj['sensor']
            from_node = self._graph.nodes.match(GraphDBService._get_label(target, model), id=target).first()
            to_node = self._graph.nodes.match(obj['object_type'], id=obj['mea_id']).first()

            rel = Relationship(from_node, 'MEASURED', to_node)
            self._graph.merge(rel) 

    @staticmethod
    def _get_label(uuid: str, model: list[dict]) -> str | None:
        for obj in model:
            if obj['uuid'] == uuid:
                return obj['object_type']
            
        return None
    
    def run(self, query: str, **parameters):
        assert self._graph is not None
        return self._graph.run(query, parameters=parameters).data()
    
    def macht_label(self, label: str):
        assert self._graph is not None
        matcher = NodeMatcher(self._graph)
        return matcher.match(label)