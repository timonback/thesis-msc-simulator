from random import Random

from .load_generator import LoadGenerator


class LoadGeneratorRandomizer(LoadGenerator):
    def __init__(self, load: LoadGenerator, variation: int = 1, seed: int = 0, only_non_zero: bool = True):
        self.load = load
        self.variation = variation
        self.only_non_zero = only_non_zero
        self.r = Random()
        self.r.seed(seed)

    def get_load_at(self, timestamp: int):
        load = self.load.get_load_at(timestamp)
        if load is 0 and self.only_non_zero is True:
            return 0
        randomized = self.r.gauss(load, self.variation)
        return int(randomized)

    def get_name(self):
        return self.load.get_name() + '_randomized'
