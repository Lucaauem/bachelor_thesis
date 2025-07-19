from database.DBFramework import DBFramework

fw = DBFramework()
fw.add_mqtt_client('CLIENT_0', 'COM-APIRadian/COM-MobileEntities/COM-Target/MEA-Position')
fw.start_client('CLIENT_0')