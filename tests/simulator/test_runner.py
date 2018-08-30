from decimal import Decimal
from unittest import TestCase

from simulator.resource.instance import InstanceTypes
from simulator.runner import SimulationRunner
from simulator.simulation_result import SimulationResult
from tests.testutil.configuration import ConfigurationUtil


class TestRunner(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config, cls.testee = cls.create_testee()

    @staticmethod
    def create_testee():
        config = ConfigurationUtil.create()
        testee = SimulationRunner(config)
        return config, testee

    def test_results_requests(self):
        results = self.get_results()

        self.assertEqual(len(results.requests), self.config.simulation_end - self.config.simulation_start)
        for index, requests_step in enumerate(results.requests):
            self.assertEqual(len(requests_step), self.config.load_altitude)
            for request in requests_step:
                self.assertEqual(request.duration, self.config.request_duration)
                self.assertEqual(request.end, index + self.config.request_duration)
                self.assertEqual(request.memory, self.config.request_memory)
                self.assertEqual(request.start, index)

    def test_results_simulations(self):
        results = self.get_results()

        for num_vms, simulation in results.simulations.items():
            instances_vm = 0
            for instances in simulation.instances:
                for instance in instances:
                    if instance.type == InstanceTypes.TYPE_VM:
                        instances_vm = instances_vm + 1
            self.assertEqual(num_vms, instances_vm)

    def test_results_fixed_values(self):
        """Attention: The values change based on the provided pricing data"""
        results = self.get_results()

        total_vms = 3
        self.assertEqual(len(results.simulations), total_vms + 1)

        price_per_vm = Decimal('0.192')
        self.assertEqual(results.simulations[total_vms].total_cost, price_per_vm * total_vms)

        self.assertEqual(results.simulations[0].total_cost, Decimal('0.0002502'))
        self.assertEqual(results.simulations[1].total_cost, Decimal('0.1921668'))
        self.assertEqual(results.simulations[2].total_cost, Decimal('0.3840834'))
        self.assertEqual(results.simulations[3].total_cost, Decimal('0.5760000'))

        self.assertEqual(self.len_vm_instances(results.simulations[3].instances[0]), 2)
        self.assertEqual(self.len_vm_instances(results.simulations[3].instances[1]), 1)
        for instances_step in results.simulations[3].instances[2:]:
            self.assertEqual(self.len_vm_instances(instances_step), 0)

        self.assertEqual(self.len_vm_instances(results.simulations[2].instances[0]), 1)
        self.assertEqual(self.len_vm_instances(results.simulations[2].instances[1]), 1)
        for instances_step in results.simulations[2].instances[2:]:
            self.assertEqual(self.len_vm_instances(instances_step), 0)

        self.assertEqual(self.len_vm_instances(results.simulations[1].instances[0]), 0)
        self.assertEqual(self.len_vm_instances(results.simulations[1].instances[1]), 1)
        for instances_step in results.simulations[1].instances[2:]:
            self.assertEqual(self.len_vm_instances(instances_step), 0)

        for instances_step in results.simulations[0].instances:
            self.assertEqual(self.len_vm_instances(instances_step), 0)

        # in a short-duration simulation. 0 vms is always the cheapest
        for num_vms, simulation in results.simulations.items():
            self.assertTrue(simulation.total_cost >= results.simulations[0].total_cost)

    def len_vm_instances(self, instances):
        return len(
            list(
                filter(
                    lambda y: y.type == InstanceTypes.TYPE_VM,
                    instances
                )
            )
        )

    def test_caching(self):
        results = self.get_results()

        self.config.plotting = False
        paths = self.testee.persist(results)
        cached = self.testee.load_cache()

        self.assertEqual(results, cached)
        self.assertEqual(len(paths), 0)

    def test_plotting(self):
        results = self.get_results()

        self.config.plotting = True
        paths = self.testee.persist(results)
        self.config.plotting = False

        self.assertEqual(len(paths), 4)

    @classmethod
    def get_results(cls) -> SimulationResult:
        if hasattr(cls, 'results') is False:
            cls.results = cls.testee.run()
        return cls.results
