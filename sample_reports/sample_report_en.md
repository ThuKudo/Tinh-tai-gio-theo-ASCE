# ASCE Wind Load Calculation Report

Based on the specified wind parameters, internal pressure coefficients, and table-derived factors, the design velocity pressure is established and combined into Case A and Case B zone pressures for frame and gable checks. Velocity pressure qz: 2.517 kN/m². Case A Z2 = -2.189 kN/m².

## Project information
- Project name: Sample report
- Project reference: WL-EN-001
- Prepared by: Thu Kudo - anhthu.phanhuynh219@gmail.com
- Generated at: 2026-03-10T16:03:49.374285+00:00

## Design criteria and code references
The design applies wind speed conversion per QCVN and ASCE, interpolation of Kz and GCpf from internal reference tables, and GCpi assignment based on enclosure classification.

## Input parameters
| Parameter | Value |
|---|---|
| Project name | Sample report |
| Project reference | WL-EN-001 |
| Design code | ASCE 7-16 |
| Wind zone | IV |
| Exposure category | B |
| Building category | III |
| Bay spacing | 1 m |
| Eave height H | 23 m |
| Roof slope i | 10 % |
| Building width Bf | 55 m |
| Building length Lf | 61.8 m |
| Enclosure classification | Enclosed |
| Source return period | 50 years |
| Target return period | 1,700 years |
| QCVN reference period | 20 years |
| Topographic factor Kzt | 1 |
| Directionality factor Kd | 0.85 |

## Assumptions
- The calculation engine applies a consistent set of wind load formulas and reference tables.
- Building category is retained for documentation, although the current model formulas do not reference it directly.
- Kz and GCpf values are obtained by linear interpolation from the internal reference tables.
- The roof-angle table is valid for the domain 0 to 90 degrees.
- Line-load labels follow a consistent one-decimal rounding rule.

## Intermediate calculations
- w0_dan_per_m2: 155.000000
- v20_mps: 50.284671
- v50_mps: 55.375697
- return_period_factor: 1.301629
- design_speed_mps: 72.078621
- design_speed_kph: 259.483034
- design_speed_mph: 161.235258
- roof_angle_deg: 5.710593
- mean_roof_height_m: 24.375000
- kz: 0.929677
- kzt: 1.000000
- kd: 0.850000
- qz_kn_per_m2: 2.516660
- gcpi_positive: 0.180000
- gcpi_negative: -0.180000

## Final results
## Final results
- Velocity pressure qz: 2.517 kN/m²
- Design speed: 72.079 m/s
- Case A Z1: WL1/WR1 = 0.569, WL2/WR2 = 1.475
- Case A Z2: WL1/WR1 = -2.189, WL2/WR2 = -1.283
- Case A Z3: WL1/WR1 = -1.397, WL2/WR2 = -0.491
- Case A Z4: WL1/WR1 = -1.2, WL2/WR2 = -0.294
- Case B Z1: WE1/WE3 = -1.585, WE2/WE4 = -0.679
- Case B Z2: WE1/WE3 = -2.189, WE2/WE4 = -1.283
- Case B Z3: WE1/WE3 = -1.384, WE2/WE4 = -0.478
- Case B Z4: WE1/WE3 = -1.585, WE2/WE4 = -0.679
- Case B Z5: WE1/WE3 = 0.554, WE2/WE4 = 1.46
- Case B Z6: WE1/WE3 = -1.183, WE2/WE4 = -0.277

## Notes / limitations
- The calculation engine applies a consistent set of wind load formulas and reference tables.
- Building category is retained for documentation, although the current model formulas do not reference it directly.
- Kz and GCpf values are obtained by linear interpolation from the internal reference tables.
- The roof-angle table is valid for the domain 0 to 90 degrees.
- Line-load labels follow a consistent one-decimal rounding rule.
- Case A windward roof currently governs a larger negative pressure than the gable case.

Prepared by: Thu Kudo - anhthu.phanhuynh219@gmail.com