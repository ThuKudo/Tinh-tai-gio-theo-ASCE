from __future__ import annotations

from html import escape
from typing import Any

from ..domain.config import FORM_SECTIONS
from ..domain.service import build_response, format_number
from ..domain.schemas import WinLoadInputSchema
from .localization import DEFAULT_LANGUAGE, get_text


def _localized_field_map(lang: str) -> dict[str, dict[str, Any]]:
    field_map: dict[str, dict[str, Any]] = {}
    for section in FORM_SECTIONS:
        for field in section["fields"]:
            field_map[field["name"]] = field
    return field_map


def _value_with_unit(value: Any, field: dict[str, Any], lang: str) -> str:
    if isinstance(value, (int, float)):
        if field["type"] == "number":
            formatted = format_number(float(value), 3).rstrip("0").rstrip(".")
        else:
            formatted = str(value)
    else:
        formatted = str(value)
    unit = field.get("unit")
    if unit == "years":
        unit = get_text(lang)["unit_years"]
    return f"{formatted} {unit}".strip() if unit and unit != "-" else formatted


def build_report_view_model(payload: WinLoadInputSchema, lang: str = DEFAULT_LANGUAGE) -> dict[str, Any]:
    result = build_response(payload, lang=lang)
    text = get_text(lang)
    field_map = _localized_field_map(lang)
    input_rows = []
    for key, value in result["inputs"].items():
        field = field_map.get(key, {"label": {lang: key}, "type": "text"})
        input_rows.append(
            {
                "name": key,
                "label": field["label"].get(lang, key),
                "value": _value_with_unit(value, field, lang),
            }
        )

    summary_metrics = [
        {"label": card["title"], "value": card["display_value"], "detail": card["detail"]} for card in result["cards"]
    ]

    case_a_governing = min(result["outputs"]["case_a"], key=lambda row: row["WL1/WR1"])
    narrative = (
        f"{text['summary_narrative']} "
        f"{text['metric_qz']}: {format_number(result['raw']['qz_kn_per_m2'], 3)} {text['unit_pressure']}. "
        f"Case A {case_a_governing['zone']} = {format_number(case_a_governing['WL1/WR1'], 3)} {text['unit_pressure']}."
    )

    report = {
        "meta": result["meta"],
        "language": lang,
        "text": text,
        "summary_narrative": narrative,
        "design_criteria": text["design_criteria_text"],
        "input_rows": input_rows,
        "summary_metrics": summary_metrics,
        "intermediate_rows": [
            {"label": key, "value": format_number(value, 6)} for key, value in result["intermediate"].items()
        ],
        "case_a_rows": result["outputs"]["case_a"],
        "case_b_rows": result["outputs"]["case_b"],
        "line_load_rows": [{"cell": k, "value": v} for k, v in result["outputs"]["line_load_labels"].items()],
        "breakdown": result["breakdown"],
        "assumptions": result["assumptions"],
        "warnings": result["warnings"] or [text["warnings_none"]],
        "result": result,
    }
    report["copy_blocks"] = build_copy_blocks(report)
    return report


def build_copy_blocks(report: dict[str, Any]) -> dict[str, str]:
    text = report["text"]
    inputs_md = ["| Parameter | Value |", "|---|---|"]
    for row in report["input_rows"]:
        inputs_md.append(f"| {row['label']} | {row['value']} |")

    breakdown_md = []
    for step in report["breakdown"]:
        breakdown_md.append(f"### {step['title']}")
        breakdown_md.append(f"- {text['breakdown_formula']}: {step['formula']}")
        breakdown_md.append(f"- {text['formula_substitute']}: {step['substitution']}")
        breakdown_md.append(f"- {text['formula_result']}: {step['result']}")
        breakdown_md.append(f"- {text['breakdown_note']}: {step['note']}")
        breakdown_md.append("")

    result_lines = [f"## {text['title_final_results']}"]
    result_lines.append(f"- {text['metric_qz']}: {format_number(report['result']['raw']['qz_kn_per_m2'], 3)} {text['unit_pressure']}")
    result_lines.append(f"- {text['metric_design_speed']}: {format_number(report['result']['raw']['design_speed_mps'], 3)} {text['unit_speed']}")
    for row in report["result"]["outputs"]["case_a"]:
        result_lines.append(f"- Case A {row['zone']}: WL1/WR1 = {row['WL1/WR1']}, WL2/WR2 = {row['WL2/WR2']}")
    for row in report["result"]["outputs"]["case_b"]:
        result_lines.append(f"- Case B {row['zone']}: WE1/WE3 = {row['WE1/WE3']}, WE2/WE4 = {row['WE2/WE4']}")

    notes_lines = ["- " + note for note in report["assumptions"]]
    if report["warnings"]:
        notes_lines.extend("- " + warning for warning in report["warnings"])

    summary_html = (
        f"<h2>{escape(text['title_calc_summary'])}</h2>"
        f"<p>{escape(report['summary_narrative'])}</p>"
        f"<p><strong>{escape(text['metric_qz'])}:</strong> {format_number(report['result']['raw']['qz_kn_per_m2'], 3)} {escape(text['unit_pressure'])}</p>"
        f"<p><strong>{escape(text['metric_design_speed'])}:</strong> {format_number(report['result']['raw']['design_speed_mps'], 3)} {escape(text['unit_speed'])}</p>"
    )

    return {
        "executive_summary": f"## {text['title_calc_summary']}\n\n{report['summary_narrative']}\n\n- {text['metric_qz']}: {format_number(report['result']['raw']['qz_kn_per_m2'], 3)} {text['unit_pressure']}\n- {text['metric_design_speed']}: {format_number(report['result']['raw']['design_speed_mps'], 3)} {text['unit_speed']}\n",
        "executive_summary_html": summary_html,
        "input_table": "\n".join(inputs_md),
        "calculation_breakdown": "\n".join(breakdown_md).strip(),
        "final_results": "\n".join(result_lines),
        "notes": "\n".join(notes_lines) if notes_lines else text["report_not_applicable"],
    }


def render_markdown(report: dict[str, Any]) -> str:
    text = report["text"]
    sections = [
        f"# {text['report_title']}",
        "",
        report["summary_narrative"],
        "",
        f"## {text['title_project_info']}",
        f"- {text['project_name']}: {report['meta']['project_name']}",
        f"- {text['project_reference']}: {report['meta']['project_reference']}",
        f"- {text['generated_at']}: {report['meta']['generated_at']}",
        "",
        f"## {text['title_design_criteria']}",
        report["design_criteria"],
        "",
        f"## {text['title_input_parameters']}",
        report["copy_blocks"]["input_table"],
        "",
        f"## {text['title_assumptions']}",
        "\n".join(f"- {item}" for item in report["assumptions"]),
        "",
        f"## {text['title_intermediate']}",
        "\n".join(f"- {row['label']}: {row['value']}" for row in report["intermediate_rows"]),
        "",
        f"## {text['title_final_results']}",
        report["copy_blocks"]["final_results"],
        "",
        f"## {text['title_notes']}",
        report["copy_blocks"]["notes"],
    ]
    return "\n".join(sections)
