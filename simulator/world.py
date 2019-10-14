from simulator.resource.instance_creator import InstanceCreator


class World:
    def __init__(self, instance_creator: InstanceCreator):
        self.instance_creator = instance_creator
        self.provisioned = list()

    def handle_requests(self, requests: list, timestamp: int):
        new_instances = self.instance_creator.create_instances(self.provisioned[:], timestamp, requests)
        self.provisioned.extend(new_instances)
        return new_instances

    def get_queued(self):
        return self.instance_creator.get_queued()
