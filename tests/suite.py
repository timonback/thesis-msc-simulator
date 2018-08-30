import logging
import unittest

from tests.simulator.load.test_load_constant import TestLoadGeneratorConstant
from tests.simulator.load.test_load_ndist import TestLoadGeneratorNDist
from tests.simulator.load.test_load_sawtooth import TestLoadGeneratorSawtooth
from tests.simulator.load.test_load_sinusoid import TestLoadGeneratorSinusoid
from tests.simulator.load.test_load_square import TestLoadGeneratorSquare
from tests.simulator.load.test_load_triangle import TestLoadGeneratorTriangle
from tests.simulator.resource.test_instance_creator_vm import TestInstanceCreatorVm
from tests.simulator.resource.test_pricing import TestPricing
from tests.simulator.test_runner import TestRunner
from tests.simulator.test_simulation_archive import TestSimulationArchive
from util.logger import setup_logging


def create_suite():
    suite = unittest.TestSuite()

    suite.addTest(unittest.makeSuite(TestLoadGeneratorConstant))
    suite.addTest(unittest.makeSuite(TestLoadGeneratorNDist))
    suite.addTest(unittest.makeSuite(TestLoadGeneratorSawtooth))
    suite.addTest(unittest.makeSuite(TestLoadGeneratorSinusoid))
    suite.addTest(unittest.makeSuite(TestLoadGeneratorSquare))
    suite.addTest(unittest.makeSuite(TestLoadGeneratorTriangle))

    suite.addTest(unittest.makeSuite(TestPricing))
    suite.addTest(unittest.makeSuite(TestInstanceCreatorVm))

    suite.addTest(unittest.makeSuite(TestSimulationArchive))

    suite.addTest(unittest.makeSuite(TestRunner))

    setup_logging('test_log.log', level=logging.INFO)

    return suite
