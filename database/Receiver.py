from datamodel.Model import Model
from database.db.DBManager import DBManager

class Receiver:
    _db_manager: DBManager

    def __init__(self, db_manager: DBManager) -> None:
        self._db_manager = db_manager
