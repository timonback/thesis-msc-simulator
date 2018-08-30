import collections

from .request_generator import RequestGenerator
from ..load.load_replay import LoadGeneratorReplay, LoadGenerator


class ReplayRequestGenerator(RequestGenerator):
    def __init__(self, requests: list):
        self.mapping = collections.defaultdict(list)

        for request in requests:
            self.mapping[request.start].append(request)

    def generate(self, amount: int, incoming_time: int, duration: float, memory: int) -> list:
        if incoming_time in self.mapping:
            return self.mapping[incoming_time]
        return list()

    def get_load(self) -> LoadGenerator:
        return LoadGeneratorReplay(self.mapping)
