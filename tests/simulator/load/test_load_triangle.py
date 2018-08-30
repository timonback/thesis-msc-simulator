from unittest import TestCase

from simulator.load.load_triangle import LoadGeneratorTriangle


class TestLoadGeneratorTriangle(TestCase):
    altitude = 10
    spacing = 20

    def create_load_generator(self):
        return LoadGeneratorTriangle(self.altitude, self.spacing)

    def test_load_values(self):
        load = self.create_load_generator()

        self.assertEqual(load.get_load_at(0), 0)
        self.assertEqual(load.get_load_at(int(self.spacing / 2)), self.altitude)
        self.assertEqual(load.get_load_at(self.spacing), 0)
