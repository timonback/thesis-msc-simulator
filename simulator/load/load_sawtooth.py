from .load_generator import LoadGenerator


class LoadGeneratorSawtooth(LoadGenerator):
    def get_load_at(self, timestamp: int):
        return self.altitude * ((timestamp % self.spacing) / (self.spacing - 1))

    def get_name(self):
        return "sawtooth"
