from database.DBFramework import DBFramework
from database.DatasetType import DatasetType

def print_msg(msg: str):
    print(msg)

fw = DBFramework()
fw.validate('[{}]', DatasetType.DATAMODEL)
#fw.add_mqtt_client('CLIENT_0', 'COM-APIRadian/COM-MobileEntities/COM-Target/MEA-Position', print_msg)
#fw.start_client('CLIENT_0')