"""Compare one-parameter effective RCMS against the full two-parameter RC-E020 model."""
from __future__ import annotations

from statistics import mean, median

from rcms.background import LCDMParams, RCMSParams
from rcms.synthetic import chi2, grid_fit_e020, grid_fit_effective, make_grid, simulate, symmetric_grid


def score_delta(chi2_ref: float, chi2_model: float, extra_params: int, n: int) -> tuple[float, float, float]:
    delta_chi2 = chi2_ref - chi2_model
    delta_aic = delta_chi2 - 2.0 * extra_params
    delta_bic = delta_chi2 - extra_params * __import__('math').log(n)
    return delta_chi2, delta_aic, delta_bic


def run_case(label: str, injected: RCMSParams | None, sigma_frac: float, seeds=range(50)) -> None:
    lcdm = LCDMParams(h0=70.0, omega_m=0.3)
    z = make_grid(2.0, 24)
    eps_grid = symmetric_grid(-0.30, 0.30, 0.02)
    s1_grid = symmetric_grid(0.2, 2.4, 0.1)
    a_grid = symmetric_grid(-0.40, 0.40, 0.01)

    full_dchi2: list[float] = []
    eff_dchi2: list[float] = []
    full_aic: list[float] = []
    eff_aic: list[float] = []
    full_bic: list[float] = []
    eff_bic: list[float] = []
    a_rec: list[float] = []

    for seed in seeds:
        data = simulate(z, lcdm, injected, fractional_sigma=sigma_frac, seed=seed)
        ref_chi2 = chi2(data, lcdm)
        _, full_chi2 = grid_fit_e020(data, lcdm, eps_grid, s1_grid)
        best_eff, eff_chi2 = grid_fit_effective(data, lcdm, a_grid)

        d2, daic, dbic = score_delta(ref_chi2, full_chi2, 2, len(data))
        full_dchi2.append(d2); full_aic.append(daic); full_bic.append(dbic)
        d2, daic, dbic = score_delta(ref_chi2, eff_chi2, 1, len(data))
        eff_dchi2.append(d2); eff_aic.append(daic); eff_bic.append(dbic)
        a_rec.append(best_eff.a_r)

    print(f"[{label}]")
    print(f"  full: delta_chi2 mean={mean(full_dchi2):.6f} median={median(full_dchi2):.6f}")
    print(f"  full: AIC-favor fraction={sum(x>0 for x in full_aic)/len(full_aic):.3f}")
    print(f"  full: BIC-favor fraction={sum(x>0 for x in full_bic)/len(full_bic):.3f}")
    print(f"  effective: delta_chi2 mean={mean(eff_dchi2):.6f} median={median(eff_dchi2):.6f}")
    print(f"  effective: AIC-favor fraction={sum(x>0 for x in eff_aic)/len(eff_aic):.3f}")
    print(f"  effective: BIC-favor fraction={sum(x>0 for x in eff_bic)/len(eff_bic):.3f}")
    print(f"  effective: A_R mean={mean(a_rec):.6f} median={median(a_rec):.6f}")


if __name__ == "__main__":
    run_case("null-LambdaCDM", None, 0.03)
    run_case("injected-RC-E020", RCMSParams(epsilon_r=0.16, s1=1.2), 0.02)
