from model import create_model
from database.DBFramework import DBFramework
from database.callbacks.Events import Events as CallbackEvents
from typing import Any, Callable
import json

def main():
    tests()
    exit(0)

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