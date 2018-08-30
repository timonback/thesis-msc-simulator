from .load_generator import LoadGenerator


class LoadGeneratorTriangle(LoadGenerator):
    def get_load_at(self, timestamp: int):
        period_step = timestamp % self.spacing
        if period_step < self.spacing / 2:
            return 2 * self.altitude * period_step / self.spacing
        return 2 * (self.altitude - (self.altitude * period_step / self.spacing))

    def get_name(self):
        return "triangle"
