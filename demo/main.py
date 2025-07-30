import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from demo.model import create_model
from database.DBFramework import DBFramework
from database.callbacks.Events import Events as CallbackEvents
from datamodel.Model import Model
from typing import Any, Callable
from demo.ML import ML

def main():
    model = create_model()
    ml = ML()
    app = DBFramework()

    # Custom callbacks for ML integration
    def insert_virtal_sensor(model):
        datamodel = Model.parse(model)
        specification = datamodel.get_object('PSP_1')
        ml.create_virtual_sensor(datamodel, 'MACHINE_1', specification)
        app.update_model(datamodel.serialize(), False)

    def update_ml_model(sensor_reading):
        ml.insert_data(sensor_reading)

    app.Callbacks.add(insert_virtal_sensor, CallbackEvents.MODEL_UPDATE)
    app.Callbacks.add(update_ml_model, CallbackEvents.NEW_SENSOR_READING)

    # Framework configuration
    tsdb = app.DB.add_tsdb('./demo/service_config/databases/influx.toml')
    graphdb = app.DB.add_graphdb('./demo/service_config/databases/neo.toml')
    app.DB.set_tsdb(tsdb)
    app.DB.set_graphdb(graphdb)
    app.clear_model()
    app.update_model(model.serialize())
    app.MQTT.add_client('./demo/service_config/mqtt/client.toml')
    app.start()

    #output = app.Fetch.batches()
    #print(output.status)
    #with open('./output.json', 'w') as f:
    #    json.dump(output.data, f, indent=2)

def check_test(title: str, callable: Callable, excpeted: Any, **parameters):
    prefix = f'TEST [{title}]:'

    if callable(**parameters) != excpeted:
        print(f'{prefix} FAILED')
        print(parameters)
        exit(1)

    print(f'{prefix} SUCCESS')

if __name__ == '__main__':
    main()