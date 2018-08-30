class InstanceCreator:
    def __init__(self):
        self.queued = list()

    def create_instances(self, provisioned: list, start: int, requests: list):
        raise NotImplementedError("Should have implemented this")

    def get_queued(self):
        return self.queued
