class LoadGenerator:
    def __init__(self, altitude: int = -1, spacing: int = -1):
        if altitude is not -1:
            self.altitude = altitude
        if spacing is not -1:
            self.spacing = spacing
        self.cumulative_cache = []

    def invalidate_cache(self):
        self.cumulative_cache = []

    def get_load_interval(self, timestamp: int, last_timestamp: int = -1) -> int:
        if last_timestamp < 0:
            last_timestamp = timestamp + last_timestamp
        interval_start = self.get_cache_or_calc_at(last_timestamp)
        interval_end = self.get_cache_or_calc_at(timestamp)
        return int(interval_end) - int(interval_start)

    def get_cache_or_calc_at(self, timestamp: int) -> int:
        if timestamp < 0:
            return 0
        try:
            return self.cumulative_cache[timestamp]
        except IndexError as e:
            previous = self.get_cache_or_calc_at(timestamp - 1)
            current = self.get_load_at(timestamp)
            cumulative = previous + current
            self.cumulative_cache.insert(timestamp, cumulative)
            return cumulative

    def get_load_at(self, timestamp: int) -> int:
        raise NotImplementedError("Should have implemented this")

    def get_name(self):
        raise NotImplementedError('Implement this')
