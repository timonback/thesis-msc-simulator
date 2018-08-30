from decimal import Decimal
from unittest import TestCase

from simulator.resource.pricing import Pricing


class TestPricing(TestCase):
    PRECISION = 10
    altitude = 10
    spacing = 20

    def create_testee(self):
        return Pricing(Pricing.CONFIG_VM)

    def test_get_price(self):
        testee = self.create_testee()
        cost, memory, btu, dynamic = testee.get_price(700)

        self.assertAlmostEqual(cost, Decimal('0.192'), 10)
        self.assertEqual(memory, 16384)
        self.assertEqual(btu, 3600)
        self.assertEqual(dynamic, False)

    def test_file_exists(self):
        testee = self.create_testee()
        self.assertEqual(testee.get_max_duration(), 3600)
