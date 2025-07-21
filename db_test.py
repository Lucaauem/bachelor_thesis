from database.DBFramework import DBFramework
from database.DatasetType import DatasetType
from database.db.DBService import TSDBService

def print_msg(msg: str):
    print(msg)

fw = DBFramework()
fw.validate('[{}]', DatasetType.DATAMODEL)

token = 'G2MjEfX9eisYzMgYtn5C_sZD4YmK_SPhS9B1ilQG8QGqa8XYdaGDNz7vykZpeeqPSXEHObPw61KrNMYF44JcBQ=='
url="http://localhost:8086"
org="my-org"

db = TSDBService(url, token, org)
db.write()


#fw.add_mqtt_client('CLIENT_0', 'COM-APIRadian/COM-MobileEntities/COM-Target/MEA-Position', print_msg)
#fw.start_client('CLIENT_0')