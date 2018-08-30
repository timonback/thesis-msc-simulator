from unittest import TestCase

from simulator.resource.instance_creator_vm import InstanceCreatorVm
from tests.testutil.configuration import ConfigurationUtil
from tests.testutil.instance_vm import InstanceVmUtil
from tests.testutil.request import RequestUtil


class TestInstanceCreatorVm(TestCase):
    def setUp(self):
        self.config, self.testee = self.create_testee()
        self.instance_vm_util = InstanceVmUtil()
        self.request_util = RequestUtil()

    @staticmethod
    def create_testee():
        config = ConfigurationUtil.create()
        testee = InstanceCreatorVm(config)
        return config, testee

    def test_min_instances(self):
        self.config.vm_min_instances = 2
        # min_instances requires at least one active requests to get triggered. So add one
        requests = list()
        requests.append(self.request_util.create_short_request())

        new_instances = self.testee.create_instances(list(), 0, requests)

        self.assertEqual(len(new_instances), 2)
        self.assertEqual(len(self.testee.queued), 0)

    def test_create_no_unnecessary_instances(self):
        new_instances = self.testee.create_instances(list(), 0, list())

        self.assertEqual(len(new_instances), 0)
        self.assertEqual(len(self.testee.queued), 0)

    def test_create_instance_use_existing(self):
        instances = list()
        instances.append(self.instance_vm_util.create_instance())

        requests = list()
        requests.append(self.request_util.create_short_request())

        new_instances = self.testee.create_instances(instances, 0, list())

        self.assertEqual(len(new_instances), 0)
        self.assertEqual(len(self.testee.queued), 0)

    def test_create_instance_after_expiration(self):
        instances = list()
        instances.append(self.instance_vm_util.create_instance())

        requests = list()
        requests.append(self.request_util.create_short_request())
        requests[0].start = 2000

        new_instances = self.testee.create_instances(instances, 3599, requests)
        self.assertEqual(len(new_instances), 0)

        new_instances = self.testee.create_instances(instances, 3600, requests)
        self.assertEqual(len(new_instances), 1)
        self.assertEqual(len(self.testee.queued), 0)

    def test_queue_unhandable_request(self):
        requests = list()
        requests.append(self.request_util.create_long_request())

        new_instances = self.testee.create_instances(list(), 0, requests)

        self.assertEqual(len(new_instances), 0)
        self.assertEqual(len(self.testee.queued), 1)
