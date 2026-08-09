# RCMS Protocol 02 — T3/T4 Results

## T3 — Pantheon+ redshift split

The preregistered split at `z_CMB = 0.3` produced:

- low-z SN + BAO: `A_R = 0.248686`, profile `[0.127307, 0.373342]`, `Delta chi2 = 4.318425`;
- high-z SN + BAO: `A_R = 0.383249`, profile `[0.214003, 0.562136]`, `Delta chi2 = 5.503936`;
- H(z) + low-z SN + BAO: `A_R = 0.244611`, profile `[0.123791, 0.368686]`, `Delta chi2 = 4.213560`;
- H(z) + high-z SN + BAO: `A_R = 0.373225`, profile `[0.205829, 0.550033]`, `Delta chi2 = 5.320252`.

No sign reversal occurred. Both redshift halves prefer positive best-fit `A_R`, with a larger amplitude in the high-z subset.

## T4 — Covariance ablation

Production full-covariance baseline:

- `A_R = 0.187021`, profile `[0.098671, 0.276779]`, `Delta chi2 = 4.559528`.

Diagnostics:

- Pantheon+ diagonal-only: `A_R = 0.253942`, movement `+0.066921`, `Delta chi2 = 12.748141`;
- BAO diagonal-only: `A_R = 0.189771`, movement `+0.002749`, `Delta chi2 = 4.221895`;
- Pantheon+ + BAO diagonal-only: `A_R = 0.256131`, movement `+0.069110`, `Delta chi2 = 11.492614`.

Interpretation: BAO covariance removal has little effect on `A_R`, while removing Pantheon+ correlations substantially increases the apparent likelihood gain. Therefore the full Pantheon+ covariance is scientifically material and remains mandatory for production inference.

These diagnostics do not alter the Protocol 02 model or decision framework.