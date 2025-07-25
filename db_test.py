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
#fw.clear_model()

fw.set_model(model)
fw.Fetch.complete_model()
#mqtt = fw.MQTT.add_client('./components/mqtt/client.toml')
#fw.launch()
