from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .domain import ExportRequestSchema, WinLoadInputSchema, build_response, form_config, report_filename
from .reporting.localization import DEFAULT_LANGUAGE
from .reporting.pdf_export import build_pdf
from .reporting.report_builder import build_report_view_model, render_markdown


if getattr(sys, "frozen", False):
    BASE_DIR = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)) / "app"
else:
    BASE_DIR = Path(__file__).resolve().parent

TEMPLATES_DIR = BASE_DIR / "web" / "templates"
STATIC_DIR = BASE_DIR / "web" / "static"

app = FastAPI(
    title="Win Load ASCE App",
    version="1.0.0",
    description="Production-ready web app for ASCE wind load checks.",
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "page_title": "Win Load ASCE",
            "page_description": "ASCE wind load checks with structured inputs, technical outputs, and professional report export.",
        },
    )


@app.get("/api/form-config")
def get_form_config() -> JSONResponse:
    return JSONResponse(form_config())


@app.get("/api/sample-input")
def get_sample_input() -> JSONResponse:
    return JSONResponse(form_config()["defaults"])


@app.post("/api/calculate")
def calculate(payload: WinLoadInputSchema, lang: str = Query(DEFAULT_LANGUAGE)) -> JSONResponse:
    return JSONResponse(build_response(payload, lang=lang))


@app.post("/api/report/html", response_class=HTMLResponse)
def export_html_report(request: Request, payload: ExportRequestSchema, lang: str = Query(DEFAULT_LANGUAGE)) -> HTMLResponse:
    report = build_report_view_model(payload.inputs, lang=lang)
    return templates.TemplateResponse(
        request=request,
        name="report.html",
        context={
            "report": report,
        },
        headers={"Content-Disposition": f"attachment; filename={report_filename(report['meta']['project_name'])}"},
    )


@app.post("/api/report/markdown")
def export_markdown_report(payload: ExportRequestSchema, lang: str = Query(DEFAULT_LANGUAGE)) -> Response:
    report = build_report_view_model(payload.inputs, lang=lang)
    markdown = render_markdown(report)
    filename = report_filename(report["meta"]["project_name"]).replace(".html", ".md")
    return Response(
        content=markdown,
        media_type="text/markdown; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@app.post("/api/report/pdf")
def export_pdf_report(payload: ExportRequestSchema, lang: str = Query(DEFAULT_LANGUAGE)) -> Response:
    report = build_report_view_model(payload.inputs, lang=lang)
    pdf = build_pdf(report)
    filename = report_filename(report["meta"]["project_name"]).replace(".html", ".pdf")
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@app.post("/api/report/blocks")
def report_blocks(payload: ExportRequestSchema, lang: str = Query(DEFAULT_LANGUAGE)) -> JSONResponse:
    report = build_report_view_model(payload.inputs, lang=lang)
    return JSONResponse({"blocks": report["copy_blocks"], "text": report["text"]})
