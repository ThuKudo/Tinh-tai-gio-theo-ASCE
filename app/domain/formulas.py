from __future__ import annotations

import math
from decimal import Decimal, ROUND_HALF_UP

from .models import PressureResult, WinLoadInputs, WindComputationResult


WIND_ZONE_TO_W0 = {
    "I": 65.0,
    "II": 95.0,
    "III": 125.0,
    "IV": 155.0,
}

KZ_TABLE = (
    (0.0, 0.7, 0.85, 1.03),
    (4.6, 0.7, 0.85, 1.03),
    (6.1, 0.7, 0.9, 1.08),
    (7.6, 0.7, 0.94, 1.12),
    (9.1, 0.7, 0.98, 1.16),
    (12.2, 0.76, 1.04, 1.22),
    (15.2, 0.81, 1.09, 1.27),
    (15.2, 0.81, 1.09, 1.27),
    (18.0, 0.85, 1.13, 1.31),
    (21.3, 0.89, 1.17, 1.34),
    (24.4, 0.93, 1.21, 1.38),
    (27.4, 0.96, 1.24, 1.4),
    (30.5, 0.99, 1.26, 1.43),
    (36.6, 1.04, 1.31, 1.48),
    (42.7, 1.09, 1.36, 1.52),
    (48.8, 1.13, 1.39, 1.55),
    (54.9, 1.17, 1.43, 1.58),
    (61.0, 1.2, 1.46, 1.61),
    (76.2, 1.28, 1.53, 1.68),
    (91.4, 1.35, 1.59, 1.73),
    (106.7, 1.41, 1.64, 1.78),
    (121.9, 1.47, 1.69, 1.82),
    (137.2, 1.52, 1.73, 1.86),
    (152.4, 1.56, 1.77, 1.89),
)

ROOF_ANGLE_TABLE = (
    (0.0, 0.4, -0.69, -0.37, -0.29),
    (5.0, 0.4, -0.69, -0.37, -0.29),
    (20.0, 0.53, -0.69, -0.48, -0.43),
    (30.0, 0.56, 0.21, -0.43, -0.37),
    (45.0, 0.56, 0.21, -0.43, -0.37),
    (90.0, 0.56, 0.56, -0.37, -0.37),
)

GABLE_CASE_B_COEFFICIENTS = {
    "z1": -0.45,
    "z2": -0.69,
    "z3": -0.37,
    "z4": -0.45,
    "z5": 0.4,
    "z6": -0.29,
}


def ns_doc(table: tuple[tuple[float, ...], ...], x: float, column_index_1_based: int) -> float:
    if column_index_1_based < 1:
        raise ValueError("column_index_1_based must be >= 1")
    ascending = table[1][0] > table[0][0]
    i = 0
    if ascending:
        while i < len(table) and table[i][0] <= x:
            i += 1
    else:
        while i < len(table) and table[i][0] >= x:
            i += 1
    if i == 0 or i >= len(table):
        raise ValueError(f"x={x} is outside interpolation domain")
    x0 = table[i - 1][0]
    x1 = table[i][0]
    y0 = table[i - 1][column_index_1_based - 1]
    y1 = table[i][column_index_1_based - 1]
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def excel_round(value: float, digits: int) -> float:
    quantize_pattern = Decimal("1").scaleb(-digits)
    return float(Decimal(str(value)).quantize(quantize_pattern, rounding=ROUND_HALF_UP))


def wind_pressure_qcvn(wind_zone: str) -> float:
    return WIND_ZONE_TO_W0.get(wind_zone, 0.0)


def speed_from_pressure(w0_dan_per_m2: float) -> float:
    return math.sqrt(w0_dan_per_m2 / 0.0613)


def qcvn_v50_speed(v20_mps: float, qcvn_reference_years: float) -> float:
    return v20_mps / (0.36 + 0.1 * math.log(12.0 * qcvn_reference_years))


def asce_return_period_factor(
    design_code: str,
    source_return_period_years: float,
    target_return_period_years: float,
) -> float:
    if design_code == "ASCE 7-10":
        numerator = 0.36 + 0.1 * math.log(12.0 * target_return_period_years)
        denominator = 0.36 + 0.1 * math.log(12.0 * source_return_period_years)
        return numerator / denominator
    numerator = 0.45 + 0.085 * math.log(12.0 * target_return_period_years)
    denominator = 0.45 + 0.085 * math.log(12.0 * source_return_period_years)
    return numerator / denominator


def roof_angle_deg(roof_slope_percent: float) -> float:
    return math.degrees(math.atan(roof_slope_percent / 100.0))


def mean_roof_height_m(eave_height_m: float, building_width_m: float, roof_slope_percent: float) -> float:
    return eave_height_m + 0.25 * building_width_m * roof_slope_percent / 100.0


def kz_from_height(mean_roof_height_m: float, exposure_category: str) -> float:
    column_lookup = {"B": 2, "C": 3, "D": 4}
    return ns_doc(KZ_TABLE, mean_roof_height_m, column_lookup[exposure_category])


def qz_kn_per_m2(kz: float, kzt: float, kd: float, design_speed_mps: float) -> float:
    return 0.613 * kz * kzt * kd * design_speed_mps**2 / 1000.0


def gcpi_pair(enclosure_type: str) -> tuple[float, float]:
    if enclosure_type == "Open":
        return 0.0, 0.0
    if enclosure_type == "Enclosed":
        return 0.18, -0.18
    return 0.55, -0.55


def gcpf_case_a(roof_angle: float, zone_number: int) -> float:
    return ns_doc(ROOF_ANGLE_TABLE, roof_angle, zone_number)


def pressure(qz: float, gc_pf: float, gc_pi: float) -> float:
    return qz * (gc_pf - gc_pi)


def line_load_label(zone_name: str, pressure_value: float, bay_spacing: float) -> str:
    return f"{zone_name}= {excel_round(pressure_value * bay_spacing, 1):.1f}"


def compute(inputs: WinLoadInputs) -> WindComputationResult:
    w0 = wind_pressure_qcvn(inputs.wind_zone)
    v20 = speed_from_pressure(w0)
    v50 = qcvn_v50_speed(v20, inputs.qcvn_reference_years)
    period_factor = asce_return_period_factor(
        inputs.design_code,
        inputs.source_return_period_years,
        inputs.target_return_period_years,
    )
    design_speed_mps = v50 * period_factor
    design_speed_kph = design_speed_mps * 3.6
    design_speed_mph = design_speed_kph * 0.6213711
    angle = roof_angle_deg(inputs.roof_slope_percent)
    mean_height = mean_roof_height_m(
        inputs.eave_height_m,
        inputs.building_width_m,
        inputs.roof_slope_percent,
    )
    kz = kz_from_height(mean_height, inputs.exposure_category)
    qz = qz_kn_per_m2(kz, inputs.topographic_factor, inputs.wind_directionality_factor, design_speed_mps)
    gcpi_pos, gcpi_neg = gcpi_pair(inputs.enclosure_type)

    case_a_gc = {
        "z1": gcpf_case_a(angle, 2),
        "z2": gcpf_case_a(angle, 3),
        "z3": gcpf_case_a(angle, 4),
        "z4": gcpf_case_a(angle, 5),
    }

    case_a_z1_wl1 = 0.0 if inputs.enclosure_type == "Open" else pressure(qz, case_a_gc["z1"], gcpi_pos)
    case_a_z1_wl2 = 0.0 if inputs.enclosure_type == "Open" else pressure(qz, case_a_gc["z1"], gcpi_neg)
    case_a_z2_wl1 = pressure(qz, case_a_gc["z2"], gcpi_pos)
    case_a_z2_wl2 = pressure(qz, case_a_gc["z2"], gcpi_neg)
    case_a_z3_wl1 = pressure(qz, case_a_gc["z3"], gcpi_pos)
    case_a_z3_wl2 = pressure(qz, case_a_gc["z3"], gcpi_neg)
    case_a_z4_wl1 = 0.0 if inputs.enclosure_type == "Open" else pressure(qz, case_a_gc["z4"], gcpi_pos)
    case_a_z4_wl2 = 0.0 if inputs.enclosure_type == "Open" else pressure(qz, case_a_gc["z4"], gcpi_neg)

    case_b_z1_we1 = 0.0 if inputs.enclosure_type == "Open" else pressure(qz, GABLE_CASE_B_COEFFICIENTS["z1"], gcpi_pos)
    case_b_z1_we2 = 0.0 if inputs.enclosure_type == "Open" else pressure(qz, GABLE_CASE_B_COEFFICIENTS["z1"], gcpi_neg)
    case_b_z2_we1 = pressure(qz, GABLE_CASE_B_COEFFICIENTS["z2"], gcpi_pos)
    case_b_z2_we2 = pressure(qz, GABLE_CASE_B_COEFFICIENTS["z2"], gcpi_neg)
    case_b_z3_we1 = pressure(qz, GABLE_CASE_B_COEFFICIENTS["z3"], gcpi_pos)
    case_b_z3_we2 = pressure(qz, GABLE_CASE_B_COEFFICIENTS["z3"], gcpi_neg)
    case_b_z4_we1 = 0.0 if inputs.enclosure_type == "Open" else pressure(qz, GABLE_CASE_B_COEFFICIENTS["z4"], gcpi_pos)
    case_b_z4_we2 = 0.0 if inputs.enclosure_type == "Open" else pressure(qz, GABLE_CASE_B_COEFFICIENTS["z4"], gcpi_neg)
    case_b_z5_we1 = 0.0 if inputs.enclosure_type == "Open" else pressure(qz, GABLE_CASE_B_COEFFICIENTS["z5"], gcpi_pos)
    case_b_z5_we2 = 0.0 if inputs.enclosure_type == "Open" else pressure(qz, GABLE_CASE_B_COEFFICIENTS["z5"], gcpi_neg)
    case_b_z6_we1 = 0.0 if inputs.enclosure_type == "Open" else pressure(qz, GABLE_CASE_B_COEFFICIENTS["z6"], gcpi_pos)
    case_b_z6_we2 = 0.0 if inputs.enclosure_type == "Open" else pressure(qz, GABLE_CASE_B_COEFFICIENTS["z6"], gcpi_neg)

    return WindComputationResult(
        w0_dan_per_m2=w0,
        v20_mps=v20,
        v50_mps=v50,
        return_period_factor=period_factor,
        design_speed_mps=design_speed_mps,
        design_speed_kph=design_speed_kph,
        design_speed_mph=design_speed_mph,
        roof_angle_deg=angle,
        mean_roof_height_m=mean_height,
        kz=kz,
        kzt=inputs.topographic_factor,
        kd=inputs.wind_directionality_factor,
        qz_kn_per_m2=qz,
        gcpi_positive=gcpi_pos,
        gcpi_negative=gcpi_neg,
        case_a_z1=PressureResult(case_a_gc["z1"], case_a_z1_wl1, case_a_z1_wl2),
        case_a_z2=PressureResult(case_a_gc["z2"], case_a_z2_wl1, case_a_z2_wl2),
        case_a_z3=PressureResult(case_a_gc["z3"], case_a_z3_wl1, case_a_z3_wl2),
        case_a_z4=PressureResult(case_a_gc["z4"], case_a_z4_wl1, case_a_z4_wl2),
        case_b_z1=PressureResult(GABLE_CASE_B_COEFFICIENTS["z1"], case_b_z1_we1, case_b_z1_we2),
        case_b_z2=PressureResult(GABLE_CASE_B_COEFFICIENTS["z2"], case_b_z2_we1, case_b_z2_we2),
        case_b_z3=PressureResult(GABLE_CASE_B_COEFFICIENTS["z3"], case_b_z3_we1, case_b_z3_we2),
        case_b_z4=PressureResult(GABLE_CASE_B_COEFFICIENTS["z4"], case_b_z4_we1, case_b_z4_we2),
        case_b_z5=PressureResult(GABLE_CASE_B_COEFFICIENTS["z5"], case_b_z5_we1, case_b_z5_we2),
        case_b_z6=PressureResult(GABLE_CASE_B_COEFFICIENTS["z6"], case_b_z6_we1, case_b_z6_we2),
    )
