from unittest import TestCase

from simulator.load.load_ndist import LoadGeneratorNDist


class TestLoadGeneratorNDist(TestCase):
    altitude = 10
    spacing = 40
    total = 20

    def create_load_generator(self):
        return LoadGeneratorNDist(self.altitude, self.spacing, self.total)

    def test_load_values(self):
        load = self.create_load_generator()

        load_counter = 0
        for i in range(0, self.spacing):
            load_counter = load_counter + load.get_load_at(i)
        self.assertEqual(load_counter, self.total)
