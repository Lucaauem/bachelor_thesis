from database.DBFramework import DBFramework

def print_msg(msg: str):
    print(msg)

fw = DBFramework()
fw.add_mqtt_client('CLIENT_0', 'COM-APIRadian/COM-MobileEntities/COM-Target/MEA-Position', print_msg)
fw.start_client('CLIENT_0')