import json
from decimal import Decimal


class Pricing:
    """Configs represent the list index of the prices.json file"""
    CONFIG_FAAS = 1
    CONFIG_VM = 0

    def __init__(self, instance_type: int):
        self.path = './prices.json'
        self.index = instance_type

        with open(self.path) as pricing_file:
            self.pricing_data = json.load(pricing_file)

    def get_price(self, memory: int) -> (Decimal, int, int, bool):
        pricing_config = self.pricing_data[self.index]
        conf = -1
        for configuration in pricing_config['configurations']:
            if memory <= configuration['memory']:
                if conf is -1:
                    conf = configuration
                elif configuration['memory'] < conf['memory']:
                    conf = configuration
        cost = Decimal(conf['cost'])
        return cost, conf['memory'], pricing_config['billing_unit_steps'], pricing_config['dynamic_duration']

    def get_vm_price(self) -> (Decimal, int, int, bool):
        pricing_config = self.pricing_data[self.index]
        conf = -1
        for configuration in pricing_config['configurations']:
            if conf is -1:
                conf = configuration
            elif configuration['memory'] < conf['memory']:
                conf = configuration
        cost = Decimal(conf['cost'])
        return cost, conf['memory'], pricing_config['billing_unit_steps'], pricing_config['dynamic_duration']

    def get_max_duration(self) -> int:
        return self.pricing_data[self.index]['billing_unit_max']
