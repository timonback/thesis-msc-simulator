from .load_generator import LoadGenerator


class LoadGeneratorSquare(LoadGenerator):
    def get_load_at(self, timestamp: int):
        spacing_half = self.spacing / 2
        period_step = timestamp % self.spacing
        if period_step < spacing_half:
            return self.altitude
        return 0

    def get_name(self):
        return "spike"
