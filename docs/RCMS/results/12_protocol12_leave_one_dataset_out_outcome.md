# RCMS Protocol 12 — Leave-One-Dataset-Family-Out Outcome

**Status:** FROZEN OUTCOME  
**Release line:** v0.3-dev  
**Classification:** `DATASET_DISTRIBUTED_POSITIVE`  
**RSMS compatibility:** RSMS-1.0-rc.1

## 1. Frozen execution

P12 used only already-frozen one-dimensional `A_R` profile summaries from five observational families and the preregistered P07-compatible asymmetric piecewise-quadratic approximation. No likelihood was refitted and no independence assumption was made.

Families:

- Moresco cosmic chronometers `H(z)`;
- Pantheon+;
- DES-SN5YR;
- eBOSS DR16;
- DESI DR2.

GitHub Actions run: `32588391090`  
Artifact: `rcms-protocol12-leave-one-dataset-out`  
Artifact ID: `9479647440`.

## 2. Full five-family descriptive profile

- common best amplitude: `A_common = 0.264069094`;
- `Delta S <= 1` interval: `[0.126078944, 0.407523584]`;
- zero in interval: `False`;
- `DeltaS_zero = 3.856261000`.

`DeltaS_zero` is a directional diagnostic only and must not be converted into a discovery significance or formal combined p-value.

## 3. Leave-one-family-out results

| Omitted family | A_common | Delta S <= 1 interval | Zero in interval | Shift from full |
|---|---:|---:|---|---:|
| HZ_MORESCO | 0.273722431 | [0.134267669, 0.417621727] | No | +0.009653337 |
| PANTHEON_PLUS | 0.277356796 | [0.123023894, 0.438680588] | No | +0.013287703 |
| DES_SN5YR | 0.235890722 | [0.089125360, 0.395557064] | No | -0.028178372 |
| EBOSS_DR16 | 0.235377310 | [0.100068842, 0.380299354] | No | -0.028691784 |
| DESI_DR2 | 0.335872173 | [0.116113043, 0.554822903] | No | +0.071803079 |

Every leave-one-family-out best fit remains positive, and every descriptive `Delta S <= 1` interval excludes zero.

## 4. Frozen classification

The preregistered `DATASET_DISTRIBUTED_POSITIVE` criteria were all satisfied:

1. full common best amplitude is positive;
2. full descriptive interval excludes zero;
3. every leave-one-family-out common best remains positive;
4. every leave-one-family-out descriptive interval excludes zero.

Therefore:

`P12_CLASSIFICATION=DATASET_DISTRIBUTED_POSITIVE`.

## 5. Scientific interpretation

Within this descriptive profile-synthesis framework, the recurring positive `A_R` direction is not eliminated by removing any one of the five named observational families. This is stronger than P07's leave-one-protocol-out check because P12 separates the negative-best-fit cosmic-chronometer family from Pantheon+ rather than using their combined P01/02 profile.

However, P12 is not a model-selection result and is not a combined significance calculation. Unknown cross-family covariance and possible observational overlap prohibit interpreting the summed profile as an independent joint likelihood.

P12 must also be read together with P11. P12 indicates that a positive smooth-deformation direction is descriptively distributed across the frozen family profiles, while P11 shows that DESI DR2 does not specifically discriminate the logarithmic RCMS function from equal-complexity smooth controls and that all tested deformations remain AIC/BIC-disfavored relative to Lambda-CDM in that test.

The scientifically defensible combined statement is therefore: a distributed positive deformation direction remains present in the frozen profile record, but its uniquely logarithmic/Resolutive interpretation is not established.
