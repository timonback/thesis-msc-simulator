from random import Random

from .request import Request
from .request_generator import RequestGenerator


class RandomRequestGenerator(RequestGenerator):
    counter = 0

    def __init__(self, variation: int = 0, seed: int = 0):
        """
        Generate requests with some variation in the execution duration (complexity)
        :param variation: Variation in percentage points (5% = 0.05)
        :param seed: Seed for the randomizer
        """
        self.variation = variation
        self.r = Random()
        self.r.seed(seed)

    def generate(self, amount: int, incoming_time: int, duration: float, memory: int) -> list:
        requests = list()
        for i in range(0, amount):
            # add a random variation
            duration_variation = 0
            if self.variation != 0:
                duration_variation = duration * self.variation * self.r.random()

            if bool(self.r.getrandbits(1)) is True:
                duration_variation = - duration_variation

            request = Request(incoming_time, duration + duration_variation, memory)
            request.id = self.counter
            self.counter = self.counter + 1
            requests.append(request)
        return requests
