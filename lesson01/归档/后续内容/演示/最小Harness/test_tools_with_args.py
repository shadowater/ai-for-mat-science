"""Check tool validation independently of grammar-constrained model output."""
import math
import unittest
from tools_with_args import circle_area, dispatch


class ParameterChecks(unittest.TestCase):
    def test_numeric_argument_controls_result(self):
        a = dispatch({'name': 'circle_area', 'arguments': {'radius_mm': 2}})
        b = dispatch({'name': 'circle_area', 'arguments': {'radius_mm': 3}})
        self.assertAlmostEqual(a['area_mm2'], 4 * math.pi)
        self.assertAlmostEqual(b['area_mm2'] / a['area_mm2'], 9 / 4)

    def test_invalid_physical_inputs(self):
        for value in [-2, True, '2', float('nan'), float('inf')]:
            with self.assertRaises(ValueError):
                circle_area(value)

    def test_unregistered_or_unexpected_requests(self):
        requests = [
            {'name': 'shell', 'arguments': {'radius_mm': 2}},
            {'name': 'circle_area', 'arguments': {}},
            {'name': 'circle_area', 'arguments': {'radius_mm': 2, 'execute': 'anything'}},
            {'name': 'circle_area', 'arguments': {'radius_mm': 2}, 'code': 'anything'},
            [],
        ]
        for request in requests:
            with self.assertRaises(ValueError):
                dispatch(request)


if __name__ == '__main__':
    unittest.main()
