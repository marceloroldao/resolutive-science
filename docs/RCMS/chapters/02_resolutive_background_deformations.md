# RCMS Chapter 2 — Resolutive Background Deformations

**Specification:** RCMS-0.1  
**Version:** 0.1-draft.2  
**Status:** Candidate-model normative draft  
**Parent:** `docs/RCMS/RCMS_v0.1.md`

---

## 2.1 Purpose

This chapter defines the first dimensionally explicit candidate family for a resolutive modification of the homogeneous cosmological expansion. Its purpose is model construction and falsification, not confirmation.

The candidate family is intentionally small. Additional flexibility shall not be added merely because a dataset is poorly fitted. A new term requires a mathematical motivation, a declared physical interpretation, and a pre-fit validation test.

## 2.2 Dimensionless state coordinates

The inherited resolutive state is

\[
R=(\rho_R,\Theta_R,\iota_R,\kappa_R).
\]

For cosmological background modeling, RCMS introduces dimensionless normalized coordinates

\[
r(z)=\frac{\rho_R(z)-\rho_{R,0}}{\rho_*},\qquad
p(z)=\frac{\Theta_R(z)-\Theta_{R,0}}{\Theta_*},
\tag{RC-E010}
\]

\[
i(z)=\frac{\iota_R(z)-\iota_{R,0}}{\iota_*},\qquad
q(z)=\frac{\kappa_R(z)-\kappa_{R,0}}{\kappa_*},
\tag{RC-E011}
\]

where each starred scale is nonzero and declared by the specialization. These normalizations do not assign physical units or interpretations to the primitive RSMS coordinates; they provide dimensionless inputs to candidate cosmological functions.

### RC-D004 — Background resolutive scalar

Define a minimal background scalar

\[
S_R(z)=\alpha_\rho r(z)+\alpha_\Theta p(z)+\alpha_\iota i(z)+\alpha_\kappa q(z),
\tag{RC-E012}
\]

where the \(\alpha\)'s are dimensionless coefficients.

RC-E012 is a model-reduction ansatz. It shall not be interpreted as proving that four primitive state components combine linearly in nature.

## 2.3 Dimensional requirement for the deformation

In

\[
H_R^2(z)=H_{\rm ref}^2(z)+\Delta_R(z),
\]

\(\Delta_R\) shall have dimensions of inverse time squared. We therefore write

\[
\Delta_R(z)=H_0^2 F_R(z),
\tag{RC-E013}
\]

where \(F_R\) is dimensionless.

This factorization is normative for the candidate family in this chapter and makes dimensional auditing explicit.

## 2.4 Candidate family

### RC-H002 — Candidate A: linear bounded deformation

\[
F_A(z)=\epsilon_R\tanh S_R(z),
\tag{RC-E014}
\]

with dimensionless amplitude \(\epsilon_R\).

Properties:

- \(|F_A|\le |\epsilon_R|\);
- the reference model is recovered for \(\epsilon_R=0\);
- for \(|S_R|\ll1\), \(F_A\approx\epsilon_R S_R\);
- the deformation cannot diverge solely because \(|S_R|\) becomes large.

Candidate A is the preferred first falsification target because it has a controlled amplitude and transparent nested reference limit.

### RC-H003 — Candidate B: even/coherence-magnitude deformation

\[
F_B(z)=\epsilon_R\left[\tanh^2 S_R(z)-\tanh^2 S_R(0)\right].
\tag{RC-E015}
\]

The subtraction fixes \(F_B(0)=0\), separating the local \(H_0\) normalization from redshift-dependent deformation. Candidate B is insensitive to the sign of \(S_R\) before the present-epoch subtraction and therefore tests a different symmetry class from Candidate A.

### RC-H004 — Candidate C: phase-sensitive bounded deformation

If a specialization assigns a meaningful dimensionless phase \(\phi_R(z)\), it may test

\[
F_C(z)=\epsilon_R\tanh S_R(z)\cos\!\left(\frac{\phi_R(z)}{2}\right).
\tag{RC-E016}
\]

The half-phase form is included only as a mathematical candidate compatible with a possible \(4\pi\)-periodic structure. RC-E016 does **not** assert that cosmological data contain a \(4\pi\) signal. Candidate C shall not be fitted until the phase evolution is independently specified; a freely adjustable phase function would be non-identifiable and nonconforming.

## 2.5 Positivity and admissibility

### RC-R006 — Positive expansion square

For every redshift in the declared fit domain,

\[
H_{\rm ref}^2(z)+H_0^2F_R(z)>0.
\tag{RC-E017}
\]

A parameter draw violating RC-E017 is inadmissible, not merely a poor fit.

### RC-R007 — Finite prediction

The candidate shall produce finite \(H_R(z)\), comoving distance, luminosity distance, and every declared BAO/CMB summary quantity throughout the validation domain.

### RC-R008 — No data-dependent functional invention

The functional form of \(F_R\) shall be frozen before observational optimization on the probe used to evaluate it. Changes motivated by residuals create a new candidate version and require a fresh validation record.

## 2.6 Minimal state evolution models

The deformation cannot be evaluated until \(S_R(z)\) is specified. To avoid fitting arbitrary functions, the first synthetic tests shall use low-complexity state evolution.

### RC-H005 — Logarithmic drift model

\[
S_R(z)=s_1\ln(1+z),
\tag{RC-E018}
\]

with one dimensionless drift coefficient \(s_1\). Since only the product of \(s_1\) and small-amplitude coefficients may be identifiable in some regimes, parameter degeneracy shall be measured explicitly.

### RC-H006 — Saturating drift model

\[
S_R(z)=s_\infty\frac{z}{1+z},
\tag{RC-E019}
\]

which approaches \(s_\infty\) at large redshift and vanishes at \(z=0\).

These are phenomenological test functions, not derived resolutive dynamics.

## 2.7 Synthetic falsification battery

Before observational fitting, each candidate shall pass the following tests.

### RC-T006 — Null recovery

Generate synthetic data from the reference cosmology. The inference pipeline shall recover \(\epsilon_R=0\) within the declared uncertainty calibration and shall not produce systematic evidence for a nonzero deformation.

### RC-T007 — Signal recovery

Generate synthetic data with known nonzero candidate parameters. The pipeline shall recover the injected deformation over a declared range of amplitudes and redshift coverage.

### RC-T008 — Wrong-model discrimination

Generate data from Candidate A and fit Candidates A and B, then reverse the experiment. Report the amplitude below which the candidates become practically indistinguishable.

### RC-T009 — Parameter identifiability

Compute posterior or likelihood correlations and profile directions for \(H_0\), reference cosmological parameters, \(\epsilon_R\), and state-evolution parameters. A parameter that is not identifiable shall not be reported as a measured physical quantity.

### RC-T010 — Numerical stability

Repeat the synthetic analysis under tighter integration tolerances, altered grids, and multiple random seeds. Numerical shifts shall remain below the declared fraction of statistical uncertainty.

### RC-T011 — Coverage / calibration

For repeated synthetic datasets, confidence or credible intervals shall be checked for their declared calibration under the generating model. Failure of interval calibration is a pipeline defect or model-assumption warning.

## 2.8 Complexity ladder

Candidates shall be tested in this order:

1. reference cosmology;
2. Candidate A + one-parameter logarithmic drift;
3. Candidate A + saturating drift;
4. Candidate B with the same drift alternatives;
5. Candidate C only after an independent phase-evolution law exists.

A more complex candidate advances only if it provides a reproducible predictive improvement that compensates for its additional flexibility under the declared comparison criteria.

## 2.9 Falsification criteria

A candidate is rejected for the tested domain if one or more of the following persist after implementation defects are excluded:

- it violates positivity or finiteness;
- it cannot recover its own injected synthetic signal;
- it spuriously detects a signal in calibrated null simulations;
- its parameters are structurally non-identifiable;
- its apparent improvement disappears out of sample;
- equivalent comparison favors the reference model after complexity penalties;
- different cosmological probes require mutually incompatible parameter regions beyond declared uncertainty.

Rejection of a candidate does not reject the RSMS mathematical framework and does not automatically reject every possible resolutive cosmology.

## 2.10 Preferred first implementation

The first implementation target shall be

\[
H_A^2(z)=H_{\rm ref}^2(z)+H_0^2\epsilon_R\tanh\!\left[s_1\ln(1+z)\right].
\tag{RC-E020}
\]

This model adds two explicit dimensionless parameters, \(\epsilon_R\) and \(s_1\), before accounting for any reference-model or nuisance parameters.

Because the small-signal regime approximately depends on the product \(\epsilon_Rs_1\), the implementation shall test this degeneracy and may define a derived effective amplitude for diagnostics. It shall not conceal the original parameterization when reporting model complexity.

## 2.11 Scientific status

RC-E020 is the **first candidate falsification model** of RCMS. It is dimensionally defined and numerically testable but is not derived from a fundamental resolutive action and is not experimentally or observationally validated.

The next stage is implementation of RC-T006 through RC-T011 on synthetic cosmological datasets before comparison with real supernova, BAO, CMB, or expansion-history observations.
