import random
from collections import Counter

from .load_generator import LoadGenerator


class LoadGeneratorNDist(LoadGenerator):
    def __init__(self, sigma: int = -1, spacing: int = -1, num_requests: int = -1, num_spikes: int = 1):
        super().__init__(sigma, spacing)
        self.num_requests = num_requests
        self.num_spikes = num_spikes

        self.mapping = dict()
        self.calc_dist()

    def calc_dist(self):
        spike_center = int(self.spacing / 2 / self.num_spikes)

        samples = self.num_requests
        if samples is -1:
            samples = self.spacing
        samples = int(samples / self.num_spikes)

        self.mapping = Counter()
        for spike_i in range(0, self.num_spikes):
            offset = int(spike_i * self.spacing / self.num_spikes)
            for i in range(0, samples):
                index = int(random.gauss(spike_center, self.altitude))
                # index = int(random.gauss(spike_center, 1.0 / self.altitude * self.spacing))
                index = offset + (index % self.spacing)  # include overlapping of the neighbouring spikes
                self.mapping[index] += 1

    def get_load_at(self, timestamp: int):
        key = timestamp % self.spacing
        return self.mapping[key]

    def get_name(self):
        return "ndist"
