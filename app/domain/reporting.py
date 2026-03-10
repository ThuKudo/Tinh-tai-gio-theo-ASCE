from __future__ import annotations

import re


def report_filename(project_name: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", project_name.strip()).strip("-").lower() or "win-load-asce"
    return f"{slug}-report.html"
