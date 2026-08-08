import math
import unittest

from rcms.background import LCDMParams, RCMSParams, h_lcdm, h_rcms_e020
from rcms.synthetic import chi2, grid_fit_e020, make_grid, simulate, symmetric_grid


class TestRCMSSynthetic(unittest.TestCase):
    def setUp(self):
        self.lcdm = LCDMParams(h0=70.0, omega_m=0.3)
        self.z = make_grid(z_max=2.0, n=24)
        self.epsilon_grid = symmetric_grid(-0.20, 0.20, 0.02)
        self.s1_grid = symmetric_grid(0.0, 2.0, 0.1)

    def test_reference_recovery_exact_at_zero_amplitude(self):
        for z in self.z:
            self.assertAlmostEqual(
                h_lcdm(z, self.lcdm),
                h_rcms_e020(z, self.lcdm, RCMSParams(epsilon_r=0.0, s1=1.3)),
                places=12,
            )

    def test_positive_expansion_guard(self):
        bad = RCMSParams(epsilon_r=-10.0, s1=10.0)
        with self.assertRaises(ValueError):
            h_rcms_e020(2.0, self.lcdm, bad)

    def test_null_recovery_does_not_force_large_signal(self):
        data = simulate(self.z, self.lcdm, rcms=None, fractional_sigma=0.03, seed=17)
        best, best_chi2 = grid_fit_e020(data, self.lcdm, self.epsilon_grid, self.s1_grid)
        ref_chi2 = chi2(data, self.lcdm, None)
        self.assertLessEqual(best_chi2, ref_chi2 + 1e-12)
        self.assertLessEqual(abs(best.epsilon_r), 0.10)

    def test_injected_signal_improves_fit(self):
        injected = RCMSParams(epsilon_r=0.16, s1=1.2)
        data = simulate(self.z, self.lcdm, rcms=injected, fractional_sigma=0.02, seed=23)
        best, best_chi2 = grid_fit_e020(data, self.lcdm, self.epsilon_grid, self.s1_grid)
        ref_chi2 = chi2(data, self.lcdm, None)
        self.assertLess(best_chi2, ref_chi2)
        self.assertGreater(best.epsilon_r, 0.0)

    def test_low_signal_degeneracy_is_present(self):
        z = 0.5
        a = RCMSParams(epsilon_r=0.10, s1=0.20)
        b = RCMSParams(epsilon_r=0.20, s1=0.10)
        ha = h_rcms_e020(z, self.lcdm, a)
        hb = h_rcms_e020(z, self.lcdm, b)
        self.assertLess(abs(ha - hb) / h_lcdm(z, self.lcdm), 5e-4)

    def test_finite_predictions_over_nominal_domain(self):
        params = RCMSParams(epsilon_r=0.20, s1=2.0)
        for z in self.z:
            value = h_rcms_e020(z, self.lcdm, params)
            self.assertTrue(math.isfinite(value))
            self.assertGreater(value, 0.0)


if __name__ == "__main__":
    unittest.main()
