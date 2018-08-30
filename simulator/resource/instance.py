from decimal import Decimal
from enum import Enum


class InstanceTypes(Enum):
    TYPE_FAAS = 0
    TYPE_VM = 1


class Instance:
    id = 0

    def __init__(self, start: int, duration: int, memory: int, cost: Decimal):
        self.id = Instance.id
        self.start = start
        self.duration = duration
        self.memory = memory
        self.cost = Decimal(cost)
        self.type = InstanceTypes.TYPE_FAAS

        Instance.id = Instance.id + 1

    @property
    def end(self) -> float:
        """The point of time, when the instances is terminated"""
        return self.start + self.duration

    @property
    def utilization(self) -> float:
        """The amount of seconds requests are being handled. Relative to others."""
        return self.duration

    def __repr__(self) -> str:
        return 'Instance[id={id}, start={start}, end={end}, memory={memory}, cost={cost}]' \
            .format(id=self.id, start=self.start, end=self.end, memory=self.memory, cost=self.cost)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Instance):
            return False
        return self.id == o.id
