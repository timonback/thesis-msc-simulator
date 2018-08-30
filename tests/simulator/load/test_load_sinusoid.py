from unittest import TestCase

from simulator.load.load_sinusoid import LoadGeneratorSinusoid


class TestLoadGeneratorSinusoid(TestCase):
    PRECISION = 10
    altitude = 10
    spacing = 20

    def create_load_generator(self):
        return LoadGeneratorSinusoid(self.altitude, self.spacing)

    def test_load_values(self):
        load = self.create_load_generator()

        baseline = self.altitude / 2
        self.assertAlmostEqual(load.get_load_at(0), baseline, self.PRECISION)
        self.assertAlmostEqual(load.get_load_at(int(self.spacing / 4)), self.altitude, self.PRECISION)
        self.assertAlmostEqual(load.get_load_at(int(self.spacing / 2)), baseline, self.PRECISION)
        self.assertAlmostEqual(load.get_load_at(int(3 * self.spacing / 4)), 0, self.PRECISION)
        self.assertAlmostEqual(load.get_load_at(self.spacing), baseline, self.PRECISION)
