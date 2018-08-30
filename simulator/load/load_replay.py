from .load_generator import LoadGenerator


class LoadGeneratorReplay(LoadGenerator):
    def __init__(self, load_mapping: dict):
        super().__init__(-1, -1)
        self.mapping = load_mapping

    def get_load_at(self, timestamp: int):
        if timestamp in self.mapping:
            return len(self.mapping[timestamp])
        return 0

    def get_name(self):
        return "replay"
