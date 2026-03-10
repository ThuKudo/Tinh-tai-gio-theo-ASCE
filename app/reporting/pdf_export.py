from __future__ import annotations

from io import BytesIO
from pathlib import Path
import unicodedata

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def _register_fonts() -> tuple[str, str]:
    local_dir = Path(__file__).resolve().parent
    candidates = [
        ("AppBundledDejaVuSans", local_dir / "DejaVuSans.ttf", local_dir / "DejaVuSans-Bold.ttf"),
        ("AppNotoSans", Path("/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"), Path("/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf")),
        ("AppDejaVuSans", Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"), Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")),
        ("AppLiberationSans", Path("/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"), Path("/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf")),
        ("AppArial", Path("C:/Windows/Fonts/arial.ttf"), Path("C:/Windows/Fonts/arialbd.ttf")),
    ]
    for family, regular, bold in candidates:
        if regular.exists() and bold.exists():
            pdfmetrics.registerFont(TTFont(family, str(regular)))
            pdfmetrics.registerFont(TTFont(f"{family}-Bold", str(bold)))
            return family, f"{family}-Bold"
    return "Helvetica", "Helvetica-Bold"


def _safe_text(value: object) -> str:
    return unicodedata.normalize("NFC", str(value))


def build_pdf(report: dict) -> bytes:
    regular_font, bold_font = _register_fonts()
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
    )
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            fontName=bold_font,
            fontSize=18,
            leading=22,
            textColor=colors.HexColor("#102033"),
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionHeading",
            parent=styles["Heading2"],
            fontName=bold_font,
            fontSize=12,
            leading=15,
            textColor=colors.HexColor("#0f4d63"),
            spaceBefore=10,
            spaceAfter=6,
        )
    )
    styles.add(ParagraphStyle(name="BodySmall", parent=styles["BodyText"], fontName=regular_font, fontSize=9.2, leading=13))

    text = report["text"]
    story = [
        Paragraph(_safe_text(text["report_title"]), styles["ReportTitle"]),
        Spacer(1, 4 * mm),
        Paragraph(_safe_text(report["summary_narrative"]), styles["BodySmall"]),
        Spacer(1, 5 * mm),
    ]

    def add_table(title: str, rows: list[list[str]], widths: list[float]) -> None:
        story.append(Paragraph(_safe_text(title), styles["SectionHeading"]))
        normalized_rows = [[_safe_text(cell) for cell in row] for row in rows]
        table = Table(normalized_rows, colWidths=widths, repeatRows=1)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eaf2f8")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#102033")),
                    ("FONTNAME", (0, 0), (-1, 0), bold_font),
                    ("FONTNAME", (0, 1), (-1, -1), regular_font),
                    ("FONTSIZE", (0, 0), (-1, -1), 8.8),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c9d5df")),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )
        story.append(table)
        story.append(Spacer(1, 4 * mm))

    add_table(
        text["title_project_info"],
        [
            [text["project_name"], report["meta"]["project_name"]],
            [text["project_reference"], report["meta"]["project_reference"]],
            [text["report_prepared_by"], f"{report['meta']['author_name']} - {report['meta']['author_email']}"],
            [text["generated_at"], report["meta"]["generated_at"]],
        ],
        [52 * mm, 120 * mm],
    )

    add_table(
        text["title_input_parameters"],
        [["Parameter", "Value"]] + [[row["label"], row["value"]] for row in report["input_rows"]],
        [68 * mm, 104 * mm],
    )

    add_table(
        text["title_intermediate"],
        [["Name", "Value"]] + [[row["label"], row["value"]] for row in report["intermediate_rows"]],
        [68 * mm, 104 * mm],
    )

    add_table(
        text["case_a_title"],
        [["Zone", "GCpf", "Case 1", "Case 2", "Line 1", "Line 2"]]
        + [
            [
                str(row["zone"]),
                str(row["gc_pf"]),
                str(row["WL1/WR1"]),
                str(row["WL2/WR2"]),
                str(row["line_load_case_1"]),
                str(row["line_load_case_2"]),
            ]
            for row in report["case_a_rows"]
        ],
        [18 * mm, 24 * mm, 30 * mm, 30 * mm, 30 * mm, 30 * mm],
    )

    add_table(
        text["case_b_title"],
        [["Zone", "GCpf", "Case 1", "Case 2", "Line 1", "Line 2"]]
        + [
            [
                str(row["zone"]),
                str(row["gc_pf"]),
                str(row["WE1/WE3"]),
                str(row["WE2/WE4"]),
                str(row["line_load_case_1"]),
                str(row["line_load_case_2"]),
            ]
            for row in report["case_b_rows"]
        ],
        [18 * mm, 24 * mm, 30 * mm, 30 * mm, 30 * mm, 30 * mm],
    )

    story.append(Paragraph(_safe_text(text["title_design_criteria"]), styles["SectionHeading"]))
    story.append(Paragraph(_safe_text(report["design_criteria"]), styles["BodySmall"]))
    story.append(Spacer(1, 3 * mm))

    story.append(Paragraph(_safe_text(text["title_assumptions"]), styles["SectionHeading"]))
    for item in report["assumptions"]:
        story.append(Paragraph(_safe_text(f"* {item}"), styles["BodySmall"]))
    story.append(Spacer(1, 3 * mm))

    story.append(Paragraph(_safe_text(text["title_notes"]), styles["SectionHeading"]))
    for item in report["warnings"]:
        story.append(Paragraph(_safe_text(f"* {item}"), styles["BodySmall"]))
    story.append(Spacer(1, 3 * mm))
    story.append(
        Paragraph(
            _safe_text(f"{text['report_prepared_by']}: {report['meta']['author_name']} - {report['meta']['author_email']}"),
            styles["BodySmall"],
        )
    )

    doc.build(story)
    return buffer.getvalue()
