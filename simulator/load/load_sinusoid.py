import math

from .load_generator import LoadGenerator


class LoadGeneratorSinusoid(LoadGenerator):
    def get_load_at(self, timestamp: int):
        shift = 0
        period = 2.0 * math.pi * timestamp / self.spacing
        value = math.sin(period + shift)
        return 0.5 * (self.altitude + (self.altitude * value))

    def get_name(self):
        return "sinusoid"
