import os, sys
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from demo.model import create_model
from database.DBFramework import DBFramework
from database.callbacks.Events import Events as CallbackEvents
from typing import Any, Callable

def main():
    tests()

    model = create_model()
    app = DBFramework()

    # Framework configuration
    tsdb = app.DB.add_tsdb('./demo/service_config/databases/influx.toml')
    graphdb = app.DB.add_graphdb('./demo/service_config/databases/neo.toml')
    app.DB.set_tsdb(tsdb)
    app.DB.set_graphdb(graphdb)
    app.clear_model()
    app.set_model(json.dumps(model.serialize()))
    app.MQTT.add_client('./demo/service_config/mqtt/client.toml')
    app.launch()

    return

    output = app.Fetch.components()
    print(output.status)
    with open('./output.json', 'w') as f:
        json.dump(output.data, f, indent=2)

def check_test(title: str, callable: Callable, excpeted: Any, **parameters):
    prefix = f'TEST [{title}]:'

    if callable(**parameters) != excpeted:
        print(f'{prefix} FAILED')
        print(parameters)
        exit(1)

    print(f'{prefix} SUCCESS')

def tests():
    print('STARTING TESTS')

    ## Blackbox tests
    # Serialisation
    ...

    # Validation

    # Output
    ...

    # Callbacks
    completed_callbacks = {event: False for event in CallbackEvents}
    app = DBFramework()

    for event in completed_callbacks.keys():
        app.Callbacks.add(lambda e=event: completed_callbacks.__setitem__(e, True), event)

    app.start()
    del app
    ...
    
    #check_test('CALLBACKS', lambda x: all(x.values()), True, x=completed_callbacks)
    
    ## Whitebox tests
    # ...
    # ...
    # ...

    print('TESTS COMPLETE!\n')

if __name__ == '__main__':
    main()