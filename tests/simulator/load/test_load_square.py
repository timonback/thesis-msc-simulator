from unittest import TestCase

from simulator.load.load_square import LoadGeneratorSquare


class TestLoadGeneratorSquare(TestCase):
    altitude = 10
    spacing = 20

    def create_load_generator(self):
        return LoadGeneratorSquare(self.altitude, self.spacing)

    def test_load_values(self):
        load = self.create_load_generator()

        for i in range(0, int(self.spacing / 2)):
            self.assertEqual(load.get_load_at(i), self.altitude)
        for i in range(int(self.spacing / 2), self.spacing):
            self.assertEqual(load.get_load_at(i), 0)
