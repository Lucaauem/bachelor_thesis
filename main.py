from model import create_model
from database.DBFramework import DBFramework
import json

def main():
    model = create_model()
    app = DBFramework()

    # Framework configuration
    tsdb = app.DB.add_tsdb('./components/databases/influx.toml')
    graphdb = app.DB.add_graphdb('./components/databases/neo.toml')
    app.DB.set_tsdb(tsdb)
    app.DB.set_graphdb(graphdb)
    app.clear_model()
    app.set_model(json.dumps(model.serialize()))
    #mqtt = app.MQTT.add_client('./components/mqtt/client.toml')
    #app.launch()

if __name__ == '__main__':
    main()