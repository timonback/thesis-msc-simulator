from .load_generator import LoadGenerator


class LoadGeneratorConstant(LoadGenerator):
    def get_load_at(self, timestamp: int):
        return self.altitude

    def get_name(self):
        return "constant"
