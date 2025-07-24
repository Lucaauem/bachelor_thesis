from database.DBFramework import DBFramework

def print_msg(msg: str):
    print(msg)

with open('./output/output.json') as f:
    model = f.read()

fw = DBFramework()
tsdb = fw.DB.add_tsdb('./components/databases/influx.toml')
graphdb = fw.DB.add_graphdb('./components/databases/neo.toml')
fw.DB.set_tsdb(tsdb)
fw.DB.set_graphdb(graphdb)

fw.set_model(model)
fw.add_mqtt_client('CLIENT_0')

fw.launch()

#with open('./dummies/soil_dummy_mea.json') as f:
#    dummy_sr = f.read()
#sr = SensorReading(dummy_sr)
#db = TSDBService("http://localhost:8086", "G2MjEfX9eisYzMgYtn5C_sZD4YmK_SPhS9B1ilQG8QGqa8XYdaGDNz7vykZpeeqPSXEHObPw61KrNMYF44JcBQ==", "my-org")
#db.add_measurement(sr)

#fw.start_client('CLIENT_0')