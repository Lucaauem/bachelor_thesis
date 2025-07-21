from database.DBFramework import DBFramework
from database.DatasetType import DatasetType
from database.db.TSDBService import TSDBService
from datamodel.soil.SensorReading import SensorReading

def print_msg(msg: str):
    print(msg)

fw = DBFramework()
fw.validate('[{}]', DatasetType.DATAMODEL)



with open('./dummies/soil_dummy_mea.json') as f:
    dummy_sr = f.read()
sr = SensorReading(dummy_sr)

db = TSDBService("http://localhost:8086", "G2MjEfX9eisYzMgYtn5C_sZD4YmK_SPhS9B1ilQG8QGqa8XYdaGDNz7vykZpeeqPSXEHObPw61KrNMYF44JcBQ==", "my-org")
db.add_measurement(sr)


#fw.add_mqtt_client('CLIENT_0', 'COM-APIRadian/COM-MobileEntities/COM-Target/MEA-Position', print_msg)
#fw.start_client('CLIENT_0')