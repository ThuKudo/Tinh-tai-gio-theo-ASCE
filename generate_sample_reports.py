from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from app.domain.schemas import WinLoadInputSchema
from app.reporting.pdf_export import build_pdf
from app.reporting.report_builder import build_report_view_model, render_markdown


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "sample_reports"


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    report_vi = build_report_view_model(WinLoadInputSchema(project_name="Bao cao mau", project_reference="WL-VI-001"), lang="vi")
    report_en = build_report_view_model(WinLoadInputSchema(project_name="Sample report", project_reference="WL-EN-001"), lang="en")

    env = Environment(loader=FileSystemLoader(str(BASE_DIR / "app" / "web" / "templates")))
    template = env.get_template("report.html")

    (OUTPUT_DIR / "sample_report_vi.html").write_text(template.render(report=report_vi), encoding="utf-8")
    (OUTPUT_DIR / "sample_report_en.html").write_text(template.render(report=report_en), encoding="utf-8")
    (OUTPUT_DIR / "sample_report_vi.md").write_text(render_markdown(report_vi), encoding="utf-8")
    (OUTPUT_DIR / "sample_report_en.md").write_text(render_markdown(report_en), encoding="utf-8")
    (OUTPUT_DIR / "sample_report_vi.pdf").write_bytes(build_pdf(report_vi))
    (OUTPUT_DIR / "sample_report_en.pdf").write_bytes(build_pdf(report_en))


if __name__ == "__main__":
    main()
