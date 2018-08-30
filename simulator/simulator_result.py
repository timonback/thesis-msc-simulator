from __future__ import annotations

import logging
from decimal import Decimal

logger = logging.getLogger(__name__)


class SimulatorResult:
    """
    Stores the result of a single simulator run.
    """
    instances_mapping = None

    def __init__(self, instances: list, queued: list):
        if len(instances) != len(queued):
            raise ValueError('The length of the parameters has to be equal. {} == {}'
                             .format(len(instances), len(queued)))

        """Amount new instances per simulation step"""
        self.instances = instances
        """Queued requests per simulation step"""
        self.queued = queued

        """Current cost per simulation step"""
        self.cost_steps = list()
        """Different types of instances"""
        self.instances_types = None
        """Total cost in USD"""
        self.total_cost = None
        """Total amount of used instances"""
        self.total_instances = None

        self.recalc()

    def recalc(self):
        """
        Calculates some properties based on constructor values
        """
        self.total_instances = 0
        self.total_cost = Decimal(0)
        for instances_step in self.instances:
            for instance in instances_step:
                self.total_cost = self.total_cost + instance.cost
                self.total_instances = self.total_instances + 1

        self.instances_types = set()
        for instances_step in self.instances:
            for instance in instances_step:
                self.instances_types.add(instance.type)
        self.instances_types = list(self.instances_types)  # trick to allow json serialization

        self.cost_steps = list()
        cost_counter = 0
        instance_counter = 0
        for step in range(0, len(self.instances)):
            for instance in self.instances[step]:
                cost_counter = cost_counter + instance.cost
                instance_counter = instance_counter + 1
            self.cost_steps.append(cost_counter)

    @staticmethod
    def merge(r1: SimulatorResult, r2: SimulatorResult) -> SimulatorResult:
        if len(r1.instances) != len(r2.instances):
            raise ValueError('The two results are not compatible. The simulation length varier1.total_instancess')

        instances = list()
        queued = list()
        for k, v in enumerate(r1.instances):
            instances.append(r1.instances[k] + r2.instances[k])
            queued.append(r1.queued[k] + r2.queued[k])
        merged = SimulatorResult(instances, queued)
        return merged

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, SimulatorResult):
            return False
        return \
            self.instances == o.instances and \
            self.queued == o.queued
