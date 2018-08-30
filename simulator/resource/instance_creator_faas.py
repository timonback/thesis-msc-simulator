import math
from decimal import Decimal

from simulator.configuration import Configuration
from simulator.resource.instance import Instance
from simulator.resource.instance_creator import InstanceCreator
from simulator.resource.pricing import Pricing


class InstanceCreatorFaaS(InstanceCreator):
    def __init__(self, config: Configuration):
        InstanceCreator.__init__(self)
        self.config = config
        self.pricing = Pricing(Pricing.CONFIG_FAAS)

    def create_instances(self, provisioned: list, start: int, requests: list):
        instances = list()
        for request in requests:
            duration = request.duration
            memory = request.memory

            cost, memory, btu, dynamic = self.pricing.get_price(memory)
            if self.pricing.get_max_duration() < duration:
                raise ValueError('Duration ({duration}) exceeds maximum possible duration ({btu})'
                                 .format(duration=duration, btu=self.pricing.get_max_duration()))

            degradation_factor = self._calc_performance_degradation_factor(memory)
            adjusted_duration = duration * degradation_factor
            btus = math.ceil(adjusted_duration / btu)
            instance = Instance(start, adjusted_duration, memory, cost * Decimal(btus))
            instances.append(instance)
        return instances

    def _calc_performance_degradation_factor(self, memory):
        return self.config.faas_performance_a + (self.config.faas_performance_m * math.log(memory))
