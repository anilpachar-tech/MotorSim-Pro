import unittest

from dc_motor import (
    calculate_efficiency,
    calculate_speed,
    calculate_torque,
    simulate_step_response,
)


class TestDCMotor(unittest.TestCase):
    def test_calculate_speed(self):
        speed = calculate_speed(12, 3, 2, 0.05, 0.1)
        self.assertAlmostEqual(speed, 11459.1559, places=2)

    def test_calculate_torque(self):
        torque = calculate_torque(5, 0.2)
        self.assertAlmostEqual(torque, 1.0, places=6)

    def test_calculate_efficiency_bounds(self):
        eff = calculate_efficiency(12, 4, 0.1, 1000)
        self.assertGreaterEqual(eff, 0.0)
        self.assertLess(eff, 100.0)

    def test_invalid_inputs_raise(self):
        with self.assertRaises(ValueError):
            calculate_speed(-1, 1, 1, 0.1, 0.1)
        with self.assertRaises(ValueError):
            calculate_torque(1, 0)
        with self.assertRaises(ValueError):
            simulate_step_response(1, 0, 0.1, 0.01, 0.0, 12)

    def test_step_response_shapes(self):
        t, rpm = simulate_step_response(2.0, 0.5, 0.1, 0.01, 0.001, 12.0, t_end=1.0)
        self.assertEqual(t.shape, rpm.shape)
        self.assertGreater(len(t), 2)


if __name__ == "__main__":
    unittest.main()
