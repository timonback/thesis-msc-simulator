from unittest import TestCase

from simulator.load.load_sawtooth import LoadGeneratorSawtooth


class TestLoadGeneratorSawtooth(TestCase):
    altitude = 10
    spacing = 20

    def create_load_generator(self):
        return LoadGeneratorSawtooth(self.altitude, self.spacing)

    def test_load_values(self):
        load = self.create_load_generator()

        self.assertEqual(load.get_load_at(0), 0)
        self.assertEqual(load.get_load_at(self.spacing - 1), self.altitude)
        self.assertEqual(load.get_load_at(self.spacing), 0)
