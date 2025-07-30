from datamodel.soil.Component import Component
from datamodel.soil.ComponentType import ComponentType
from datamodel.Model import Model
from datamodel.mmpd.resource.Machine import Machine
import os, sys
import json
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ONLY FOR DEMONSTRATION
class ML:
    def insert_data(self, dataframe) -> None:
        print('FEEDING DATA INTO ML MODEL')

    def create_virtual_sensor(self, model: Model, machine_uuid: str, parameters) -> None:
        print('CREATE NEW VSENSOR')
        with open('./demo/components/sensors/sensor_0.json') as f:
            data = json.load(f)
        
        uuid = f'VIRT_{data['uuid']}'
        data['uuid'] = uuid

        for mea in data['measurements']:
            min_val, max_val = mea['range']
            mea['value'] = [round(random.uniform(min_val, max_val), 2) for _ in range(mea['dimension'][0])]

        machine = model.get_object(machine_uuid)
        assert isinstance(machine, Machine)
        machine.add_sensor(Component(json.dumps(data), ComponentType.VIRTUAL, model))
