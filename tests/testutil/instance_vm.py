from decimal import Decimal

from simulator.resource.instance_vm import InstanceVm


class InstanceVmUtil:
    def __init__(self):
        self.start = 0
        self.end = 0
        self.memory = 128
        self.price = 0.2

    def create_instance(self):
        return InstanceVm(self.start, 3600, self.memory, Decimal(self.price))
