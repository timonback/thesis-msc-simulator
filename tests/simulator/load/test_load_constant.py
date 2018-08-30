from unittest import TestCase

from simulator.load.load_constant import LoadGeneratorConstant


class TestLoadGeneratorConstant(TestCase):
    altitude = 10
    spacing = 20

    def create_load_generator(self):
        return LoadGeneratorConstant(self.altitude, self.spacing)

    def test_load_values(self):
        load = self.create_load_generator()

        for i in range(0, 2 * self.spacing):
            self.assertEqual(load.get_load_at(i), self.altitude)
