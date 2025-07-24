from database.Log import log
from database.db.GraphDBService import GraphDBService
from database.db.TSDBService import TSDBService
import toml

class DBManager:
    _graphdb: dict[str, GraphDBService]
    _tsdb: dict[str, TSDBService]
    _active_graphdb: str = ''
    _active_tsdb: str = ''

    def __init__(self) -> None:
        self._graphdb = {}
        self._tsdb = {}

    def add_tsdb(self, toml_path: str) -> str:
        with open(toml_path) as f:
            file = toml.load(f)

        id = f'TSDB_{len(self._tsdb.keys())}'
        self._tsdb[id] = TSDBService(file['url'], file['token'], file['org'])

        return id

    def add_graphdb(self, toml_path: str) -> str:
        with open(toml_path) as f:
            file = toml.load(f)

        id = f'GRAPHDB_{len(self._graphdb.keys())}'
        self._graphdb[id] = GraphDBService(file['url'], file['user'], file['password'])

        return id

    def set_tsdb(self, id: str) -> None:
        if id not in self._tsdb.keys():
            raise KeyError(f'TSDB [{id}]: Not found!')
        
        if len(self._active_tsdb) > 0:
            active = self._tsdb[self._active_tsdb]
            log(f'TSDB [{self._active_tsdb}]: Disconnecting...')
            active.disconnect()
        
        service = self._tsdb[id]
        log(f'TSDB [{id}]: Connecting...')
        try:
            service.connect()
            self._active_tsdb = id
            log(f'TSDB [{id}]: Connected successfully!')
        except:
            log(f'TSDB [{id}]: Failed to connect!')

    def set_graphdb(self, id: str) -> None:
        if id not in self._graphdb.keys():
            raise KeyError(f'GraphDB [{id}]: Not found!')
        
        if len(self._active_graphdb) > 0:
            active = self._graphdb[self._active_graphdb]
            log(f'GraphDB [{self._active_graphdb}]: Disconnecting...')
            active.disconnect()
        
        service = self._graphdb[id]
        log(f'GraphDB [{id}]: Connecting...')
        try:
            service.connect()
            self._active_graphdb = id
            log(f'GraphDB [{id}]: Connected successfully!')
        except:
            log(f'GraphDB [{id}]: Failed to connect!')

    @property
    def active_tsdb(self) -> TSDBService:
        assert len(self._active_tsdb) > 0
        return self._tsdb[self._active_graphdb]
    
    @property
    def active_graphdb(self) -> GraphDBService:
        assert len(self._active_graphdb) > 0
        return self._graphdb[self._active_graphdb]