from datamodel.Model import Model
from database.db.DBManager import DBManager
from database.db.TSDBService import TSDBService
from database.db.GraphDBService import GraphDBService
import json

class Fetch:
    _db_manager: DBManager
    _tsdb: TSDBService
    _graphdb: GraphDBService

    def __init__(self, db_manager: DBManager) -> None:
        self._db_manager = db_manager

    def _get_current_dbs(self) -> None:
        self._tsdb = self._db_manager.active_tsdb
        self._graphdb = self._db_manager.active_graphdb

    def complete_model(self):
        self._get_current_dbs()

        data = []

        query_data = self._graphdb.run('MATCH (n) RETURN n')
        for obj in query_data:
            node = obj["n"]
            
            if node is None:
                continue

            #print(dict(node)['id'])

            node = dict(node)['data']
            node = json.loads(str(node))
            data.append(node)
        
        with open('./a.json', 'w') as f:
            json.dump(data, f, indent=2)