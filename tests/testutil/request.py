from simulator.request.request import Request


class RequestUtil:
    def __init__(self):
        self.start = 0
        self.memory = 128

    def create_short_request(self):
        return Request(self.start, 1, self.memory)

    def create_long_request(self):
        return Request(self.start, 1000000, self.memory)
