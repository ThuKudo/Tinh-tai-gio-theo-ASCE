from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WinLoadInputs:
    design_code: str
    wind_zone: str
    exposure_category: str
    building_category: str
    bay_spacing_m: float
    eave_height_m: float
    roof_slope_percent: float
    building_width_m: float
    building_length_m: float
    enclosure_type: str
    source_return_period_years: float = 50.0
    target_return_period_years: float = 1700.0
    qcvn_reference_years: float = 20.0
    topographic_factor: float = 1.0
    wind_directionality_factor: float = 0.85


@dataclass(frozen=True)
class PressureResult:
    gc_pf: float
    wl1_or_we1: float
    wl2_or_we2: float


@dataclass(frozen=True)
class WindComputationResult:
    w0_dan_per_m2: float
    v20_mps: float
    v50_mps: float
    return_period_factor: float
    design_speed_mps: float
    design_speed_kph: float
    design_speed_mph: float
    roof_angle_deg: float
    mean_roof_height_m: float
    kz: float
    kzt: float
    kd: float
    qz_kn_per_m2: float
    gcpi_positive: float
    gcpi_negative: float
    case_a_z1: PressureResult
    case_a_z2: PressureResult
    case_a_z3: PressureResult
    case_a_z4: PressureResult
    case_b_z1: PressureResult
    case_b_z2: PressureResult
    case_b_z3: PressureResult
    case_b_z4: PressureResult
    case_b_z5: PressureResult
    case_b_z6: PressureResult
