import logging
import math
from collections import Counter
from decimal import Decimal

from simulator.request.request import Request
from simulator.resource.instance import Instance, InstanceTypes

logger = logging.getLogger(__name__)


class InstanceVm(Instance):
    def __init__(self, start: int, duration: int, memory: int, cost: Decimal):
        super().__init__(start, duration, memory, cost)

        self.type = InstanceTypes.TYPE_VM
        self.requests = list()

        self.handling_at_cache = Counter()

    def handle(self, request: Request) -> bool:
        if request in self.requests:
            logger.warning('Instance {i} handles the same requests {r} again'
                           .format(i=self, r=request))
        else:
            if self.could_handle(self.start, self.duration, self.memory, request):
                self.requests.append(request)
                for i in range(request.start, math.ceil(request.end)):
                    self.handling_at_cache[i] += 1
                return True
        return False

    @staticmethod
    def could_handle(start: int, duration: int, memory: int, request: Request) -> bool:
        return \
            request.end <= start + duration and \
            request.memory <= memory

    def handling_requests_at(self, timestamp: int) -> int:
        return self.handling_at_cache[timestamp]

    @property
    def utilization(self) -> float:
        requests_seconds = 0
        for request in self.requests:
            requests_seconds = requests_seconds + request.duration
        return requests_seconds
