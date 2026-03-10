from __future__ import annotations

from dataclasses import asdict
from datetime import UTC, datetime
from typing import Any

from .config import APP_ASSUMPTIONS, FORM_SECTIONS
from .formulas import compute, excel_round, line_load_label
from .models import WinLoadInputs
from .schemas import WinLoadInputSchema
from ..reporting.localization import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES, get_text


def default_input_payload() -> dict[str, Any]:
    return WinLoadInputSchema().model_dump()


def form_config() -> dict[str, Any]:
    return {
        "sections": FORM_SECTIONS,
        "defaults": default_input_payload(),
        "assumptions": APP_ASSUMPTIONS,
        "languages": list(SUPPORTED_LANGUAGES),
        "default_language": DEFAULT_LANGUAGE,
        "ui_text": {lang: get_text(lang) for lang in SUPPORTED_LANGUAGES},
    }


def to_domain_model(payload: WinLoadInputSchema) -> WinLoadInputs:
    return WinLoadInputs(
        design_code=payload.design_code,
        wind_zone=payload.wind_zone,
        exposure_category=payload.exposure_category,
        building_category=payload.building_category,
        bay_spacing_m=payload.bay_spacing_m,
        eave_height_m=payload.eave_height_m,
        roof_slope_percent=payload.roof_slope_percent,
        building_width_m=payload.building_width_m,
        building_length_m=payload.building_length_m,
        enclosure_type=payload.enclosure_type,
        source_return_period_years=payload.source_return_period_years,
        target_return_period_years=payload.target_return_period_years,
        qcvn_reference_years=payload.qcvn_reference_years,
        topographic_factor=payload.topographic_factor,
        wind_directionality_factor=payload.wind_directionality_factor,
    )


def format_number(value: float, digits: int = 3) -> str:
    return f"{value:,.{digits}f}"


def _card(title: str, value: float, unit: str, detail: str) -> dict[str, Any]:
    return {
        "title": title,
        "value": round(value, 3),
        "display_value": f"{format_number(value, 3)} {unit}".strip(),
        "unit": unit,
        "detail": detail,
    }


def _pressure_row(zone: str, result: dict[str, float], line_factor: float, labels: tuple[str, str]) -> dict[str, Any]:
    return {
        "zone": zone,
        "gc_pf": round(result["gc_pf"], 3),
        labels[0]: round(result["wl1_or_we1"], 3),
        labels[1]: round(result["wl2_or_we2"], 3),
        "line_load_case_1": excel_round(result["wl1_or_we1"] * line_factor, 1),
        "line_load_case_2": excel_round(result["wl2_or_we2"] * line_factor, 1),
    }


def _line_load_labels(result_payload: dict[str, Any], bay_spacing_m: float) -> dict[str, str]:
    return {
        "S18": line_load_label("Z2", result_payload["case_a_z2"]["wl1_or_we1"], bay_spacing_m),
        "V18": line_load_label("Z3", result_payload["case_a_z3"]["wl1_or_we1"], bay_spacing_m),
        "Y18": line_load_label("Z2", result_payload["case_a_z2"]["wl2_or_we2"], bay_spacing_m),
        "AB18": line_load_label("Z3", result_payload["case_a_z3"]["wl2_or_we2"], bay_spacing_m),
        "S20": line_load_label("Z1", result_payload["case_a_z1"]["wl1_or_we1"], bay_spacing_m),
        "V20": line_load_label("Z4", result_payload["case_a_z4"]["wl1_or_we1"], bay_spacing_m),
        "Y20": line_load_label("Z1", result_payload["case_a_z1"]["wl2_or_we2"], bay_spacing_m),
        "AB20": line_load_label("Z4", result_payload["case_a_z4"]["wl2_or_we2"], bay_spacing_m),
        "S39": line_load_label("Z2", result_payload["case_b_z2"]["wl1_or_we1"], bay_spacing_m),
        "V39": line_load_label("Z3", result_payload["case_b_z3"]["wl1_or_we1"], bay_spacing_m),
        "Y39": line_load_label("Z2", result_payload["case_b_z2"]["wl2_or_we2"], bay_spacing_m),
        "AB39": line_load_label("Z3", result_payload["case_b_z3"]["wl2_or_we2"], bay_spacing_m),
        "S41": line_load_label("Z1", result_payload["case_b_z1"]["wl1_or_we1"], bay_spacing_m),
        "V41": line_load_label("Z4", result_payload["case_b_z4"]["wl1_or_we1"], bay_spacing_m),
        "Y41": line_load_label("Z1", result_payload["case_b_z1"]["wl2_or_we2"], bay_spacing_m),
        "AB41": line_load_label("Z4", result_payload["case_b_z4"]["wl2_or_we2"], bay_spacing_m),
    }


def build_calculation_breakdown(
    payload: WinLoadInputSchema,
    result_payload: dict[str, Any],
    lang: str,
) -> list[dict[str, Any]]:
    text = get_text(lang)
    if lang == "vi":
        items = [
            {
                "title": "Chuẩn hóa hình học đầu vào",
                "formula": "he = H + 0.25 × Bf × i / 100 ; θ = atan(i/100)",
                "substitution": f"he = {payload.eave_height_m} + 0.25 × {payload.building_width_m} × {payload.roof_slope_percent}/100 ; θ = atan({payload.roof_slope_percent}/100)",
                "result": f"he = {format_number(result_payload['mean_roof_height_m'], 3)} m ; θ = {format_number(result_payload['roof_angle_deg'], 3)} độ",
                "inputs": {"H": payload.eave_height_m, "Bf": payload.building_width_m, "i": payload.roof_slope_percent},
                "outputs": {"mean_roof_height_m": round(result_payload["mean_roof_height_m"], 6), "roof_angle_deg": round(result_payload["roof_angle_deg"], 6)},
                "note": "Bước này quy đổi hình học mái trước khi tra bảng hoặc tính áp lực.",
            },
            {
                "title": "Chuyển đổi vận tốc gió",
                "formula": "W0 → V20 → V50 → Vdesign theo công thức QCVN và ASCE",
                "substitution": f"W0 = {result_payload['w0_dan_per_m2']} ; V20 = sqrt(W0/0.0613) ; a = f({payload.design_code}, {payload.source_return_period_years}, {payload.target_return_period_years})",
                "result": f"V = {format_number(result_payload['design_speed_mps'], 3)} m/s",
                "inputs": {
                    "wind_zone": payload.wind_zone,
                    "qcvn_reference_years": payload.qcvn_reference_years,
                    "source_return_period_years": payload.source_return_period_years,
                    "target_return_period_years": payload.target_return_period_years,
                    "design_code": payload.design_code,
                },
                "outputs": {
                    "w0_dan_per_m2": round(result_payload["w0_dan_per_m2"], 6),
                    "v20_mps": round(result_payload["v20_mps"], 6),
                    "v50_mps": round(result_payload["v50_mps"], 6),
                    "return_period_factor": round(result_payload["return_period_factor"], 6),
                    "design_speed_mps": round(result_payload["design_speed_mps"], 6),
                },
                "note": "Hệ số chu kỳ lặp thay đổi theo phiên bản tiêu chuẩn ASCE được chọn.",
            },
            {
                "title": "Tra bảng và tính áp lực vận tốc",
                "formula": "Kz = NS_DOC(KZ_TABLE, he, exposure_column) ; qz = 0.613 × Kz × Kzt × Kd × V² / 1000",
                "substitution": f"Kz = NS_DOC(..., {format_number(result_payload['mean_roof_height_m'], 3)}, {payload.exposure_category}) ; qz = 0.613 × {format_number(result_payload['kz'], 6)} × {payload.topographic_factor} × {payload.wind_directionality_factor} × {format_number(result_payload['design_speed_mps'], 6)}² / 1000",
                "result": f"Kz = {format_number(result_payload['kz'], 3)} ; qz = {format_number(result_payload['qz_kn_per_m2'], 3)} kN/m²",
                "inputs": {"exposure_category": payload.exposure_category, "Kzt": payload.topographic_factor, "Kd": payload.wind_directionality_factor},
                "outputs": {"kz": round(result_payload["kz"], 6), "qz_kn_per_m2": round(result_payload["qz_kn_per_m2"], 6)},
                "note": "Hệ số được nội suy tuyến tính từ bảng tham chiếu nội bộ của phần mềm.",
            },
            {
                "title": "Tổ hợp áp lực vùng",
                "formula": "WZi = qz × (GCpf - GCpi)",
                "substitution": f"GCpi+ = {result_payload['gcpi_positive']} ; GCpi- = {result_payload['gcpi_negative']}",
                "result": "Sinh ra các áp lực vùng cho Case A và Case B.",
                "inputs": {
                    "enclosure_type": payload.enclosure_type,
                    "gcpi_positive": round(result_payload["gcpi_positive"], 6),
                    "gcpi_negative": round(result_payload["gcpi_negative"], 6),
                },
                "outputs": {"case_a_zones": [f"Z{i}" for i in range(1, 5)], "case_b_zones": [f"Z{i}" for i in range(1, 7)]},
                "note": "Nhà hở sẽ triệt tiêu một số áp lực tường theo logic điều kiện của mô hình tính.",
            },
        ]
    else:
        items = [
            {
                "title": "Input normalization",
                "formula": "he = H + 0.25 × Bf × i / 100 ; θ = atan(i/100)",
                "substitution": f"he = {payload.eave_height_m} + 0.25 × {payload.building_width_m} × {payload.roof_slope_percent}/100 ; θ = atan({payload.roof_slope_percent}/100)",
                "result": f"he = {format_number(result_payload['mean_roof_height_m'], 3)} m ; θ = {format_number(result_payload['roof_angle_deg'], 3)} deg",
                "inputs": {"H": payload.eave_height_m, "Bf": payload.building_width_m, "i": payload.roof_slope_percent},
                "outputs": {"mean_roof_height_m": round(result_payload["mean_roof_height_m"], 6), "roof_angle_deg": round(result_payload["roof_angle_deg"], 6)},
                "note": "Roof geometry is normalized before any lookup or pressure calculation.",
            },
            {
                "title": "Wind speed conversion",
                "formula": "W0 → V20 → V50 → Vdesign using the QCVN and ASCE equations",
                "substitution": f"W0 = {result_payload['w0_dan_per_m2']} ; V20 = sqrt(W0/0.0613) ; a = f({payload.design_code}, {payload.source_return_period_years}, {payload.target_return_period_years})",
                "result": f"V = {format_number(result_payload['design_speed_mps'], 3)} m/s",
                "inputs": {
                    "wind_zone": payload.wind_zone,
                    "qcvn_reference_years": payload.qcvn_reference_years,
                    "source_return_period_years": payload.source_return_period_years,
                    "target_return_period_years": payload.target_return_period_years,
                    "design_code": payload.design_code,
                },
                "outputs": {
                    "w0_dan_per_m2": round(result_payload["w0_dan_per_m2"], 6),
                    "v20_mps": round(result_payload["v20_mps"], 6),
                    "v50_mps": round(result_payload["v50_mps"], 6),
                    "return_period_factor": round(result_payload["return_period_factor"], 6),
                    "design_speed_mps": round(result_payload["design_speed_mps"], 6),
                },
                "note": "The return-period factor changes with the selected ASCE edition.",
            },
            {
                "title": "Lookup and velocity pressure",
                "formula": "Kz = NS_DOC(KZ_TABLE, he, exposure_column) ; qz = 0.613 × Kz × Kzt × Kd × V² / 1000",
                "substitution": f"Kz = NS_DOC(..., {format_number(result_payload['mean_roof_height_m'], 3)}, {payload.exposure_category}) ; qz = 0.613 × {format_number(result_payload['kz'], 6)} × {payload.topographic_factor} × {payload.wind_directionality_factor} × {format_number(result_payload['design_speed_mps'], 6)}² / 1000",
                "result": f"Kz = {format_number(result_payload['kz'], 3)} ; qz = {format_number(result_payload['qz_kn_per_m2'], 3)} kN/m²",
                "inputs": {"exposure_category": payload.exposure_category, "Kzt": payload.topographic_factor, "Kd": payload.wind_directionality_factor},
                "outputs": {"kz": round(result_payload["kz"], 6), "qz_kn_per_m2": round(result_payload["qz_kn_per_m2"], 6)},
                "note": "The coefficient is obtained by linear interpolation from the internal reference table.",
            },
            {
                "title": "Pressure combinations",
                "formula": "WZi = qz × (GCpf - GCpi)",
                "substitution": f"GCpi+ = {result_payload['gcpi_positive']} ; GCpi- = {result_payload['gcpi_negative']}",
                "result": "This produces the governing zone pressures for Case A and Case B.",
                "inputs": {
                    "enclosure_type": payload.enclosure_type,
                    "gcpi_positive": round(result_payload["gcpi_positive"], 6),
                    "gcpi_negative": round(result_payload["gcpi_negative"], 6),
                },
                "outputs": {"case_a_zones": [f"Z{i}" for i in range(1, 5)], "case_b_zones": [f"Z{i}" for i in range(1, 7)]},
                "note": "Open buildings suppress selected wall pressures according to the model condition branches.",
            },
        ]
    for item in items:
        item["formula_label"] = text["breakdown_formula"]
        item["note_label"] = text["breakdown_note"]
        item["substitute_label"] = text["formula_substitute"]
        item["result_label"] = text["formula_result"]
    return items


def build_warnings(payload: WinLoadInputSchema, result_payload: dict[str, Any], lang: str) -> list[str]:
    warnings: list[str] = []
    if payload.enclosure_type == "Open":
        warnings.append(
            "Nhà hở: một số áp lực tường được đưa về 0 theo logic điều kiện của mô hình." if lang == "vi" else "Open building: selected wall pressures are forced to zero by the model conditions."
        )
    if payload.mean_roof_height_m > 120:
        warnings.append(
            "Cao độ giữa mái nằm gần giới hạn trên của bảng Kz." if lang == "vi" else "Mean roof height is close to the upper limit of the Kz table."
        )
    if abs(result_payload["case_a_z2"]["wl1_or_we1"]) > abs(result_payload["case_b_z5"]["wl1_or_we1"]):
        warnings.append(
            "Case A mái đón gió đang chi phối áp lực âm lớn hơn đầu hồi." if lang == "vi" else "Case A windward roof currently governs a larger negative pressure than the gable case."
        )
    return warnings


def build_response(payload: WinLoadInputSchema, lang: str = DEFAULT_LANGUAGE) -> dict[str, Any]:
    lang = lang if lang in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE
    text = get_text(lang)
    domain_inputs = to_domain_model(payload)
    result_payload = asdict(compute(domain_inputs))
    labels = _line_load_labels(result_payload, payload.bay_spacing_m)

    cards = [
        _card(text["metric_design_speed"], result_payload["design_speed_mps"], text["unit_speed"], text["detail_design_speed"]),
        _card(text["metric_qz"], result_payload["qz_kn_per_m2"], text["unit_pressure"], text["detail_qz"]),
        _card(text["metric_roof_angle"], result_payload["roof_angle_deg"], "deg", text["detail_roof_angle"]),
        _card(text["metric_mean_roof_height"], result_payload["mean_roof_height_m"], text["unit_m"], text["detail_mean_roof_height"]),
        _card(text["metric_kz"], result_payload["kz"], "-", text["detail_kz"]),
        _card(text["metric_gcpi_pos"], result_payload["gcpi_positive"], "-", text["detail_gcpi_pos"]),
    ]

    case_a_rows = [
        _pressure_row("Z1", result_payload["case_a_z1"], payload.bay_spacing_m, ("WL1/WR1", "WL2/WR2")),
        _pressure_row("Z2", result_payload["case_a_z2"], payload.bay_spacing_m, ("WL1/WR1", "WL2/WR2")),
        _pressure_row("Z3", result_payload["case_a_z3"], payload.bay_spacing_m, ("WL1/WR1", "WL2/WR2")),
        _pressure_row("Z4", result_payload["case_a_z4"], payload.bay_spacing_m, ("WL1/WR1", "WL2/WR2")),
    ]
    case_b_rows = [
        _pressure_row("Z1", result_payload["case_b_z1"], payload.bay_spacing_m, ("WE1/WE3", "WE2/WE4")),
        _pressure_row("Z2", result_payload["case_b_z2"], payload.bay_spacing_m, ("WE1/WE3", "WE2/WE4")),
        _pressure_row("Z3", result_payload["case_b_z3"], payload.bay_spacing_m, ("WE1/WE3", "WE2/WE4")),
        _pressure_row("Z4", result_payload["case_b_z4"], payload.bay_spacing_m, ("WE1/WE3", "WE2/WE4")),
        _pressure_row("Z5", result_payload["case_b_z5"], payload.bay_spacing_m, ("WE1/WE3", "WE2/WE4")),
        _pressure_row("Z6", result_payload["case_b_z6"], payload.bay_spacing_m, ("WE1/WE3", "WE2/WE4")),
    ]

    warnings = build_warnings(payload, result_payload, lang)

    return {
        "meta": {
            "project_name": payload.project_name,
            "project_reference": payload.project_reference,
            "generated_at": datetime.now(UTC).isoformat(),
            "language": lang,
        },
        "language": lang,
        "text": text,
        "inputs": payload.model_dump(),
        "cards": cards,
        "intermediate": {
            "w0_dan_per_m2": round(result_payload["w0_dan_per_m2"], 6),
            "v20_mps": round(result_payload["v20_mps"], 6),
            "v50_mps": round(result_payload["v50_mps"], 6),
            "return_period_factor": round(result_payload["return_period_factor"], 6),
            "design_speed_mps": round(result_payload["design_speed_mps"], 6),
            "design_speed_kph": round(result_payload["design_speed_kph"], 6),
            "design_speed_mph": round(result_payload["design_speed_mph"], 6),
            "roof_angle_deg": round(result_payload["roof_angle_deg"], 6),
            "mean_roof_height_m": round(result_payload["mean_roof_height_m"], 6),
            "kz": round(result_payload["kz"], 6),
            "kzt": round(result_payload["kzt"], 6),
            "kd": round(result_payload["kd"], 6),
            "qz_kn_per_m2": round(result_payload["qz_kn_per_m2"], 6),
            "gcpi_positive": round(result_payload["gcpi_positive"], 6),
            "gcpi_negative": round(result_payload["gcpi_negative"], 6),
        },
        "outputs": {
            "case_a": case_a_rows,
            "case_b": case_b_rows,
            "line_load_labels": labels,
        },
        "breakdown": build_calculation_breakdown(payload, result_payload, lang),
        "assumptions": APP_ASSUMPTIONS[lang],
        "warnings": warnings,
        "raw": result_payload,
    }
