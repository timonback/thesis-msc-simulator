from unittest import TestCase

from simulator.simulation_archive import SimulationArchive
from simulator.simulation_result import SimulationResult
from tests.testutil.configuration import ConfigurationUtil


class TestSimulationArchive(TestCase):
    def create_testee(self):
        config = ConfigurationUtil.create()
        config.simulation_end = -1  # invalid configuration to not let others possibly load this
        testee = SimulationArchive(config)
        return testee, config

    def test_exists(self):
        testee, config = self.create_testee()

        testee.remove(config)

        self.assertFalse(testee.exists(config))

    def test_archive(self):
        testee, config = self.create_testee()
        result = SimulationResult(config, list())

        testee.save(result)
        self.assertTrue(testee.exists(config))

        loaded = testee.retrieve(config)
        self.assertEqual(result, loaded)
