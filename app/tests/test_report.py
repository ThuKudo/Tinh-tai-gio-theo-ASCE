from __future__ import annotations

import unittest

from app.domain.schemas import WinLoadInputSchema
from app.reporting.pdf_export import build_pdf
from app.reporting.report_builder import build_report_view_model, render_markdown


class ReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report_vi = build_report_view_model(WinLoadInputSchema(project_name="Bao cao mau"), lang="vi")
        cls.report_en = build_report_view_model(WinLoadInputSchema(project_name="Sample report"), lang="en")

    def test_report_builds_successfully(self) -> None:
        self.assertIn("summary_narrative", self.report_vi)
        self.assertTrue(self.report_vi["case_a_rows"])
        self.assertTrue(self.report_vi["copy_blocks"])

    def test_key_sections_exist_in_markdown(self) -> None:
        markdown = render_markdown(self.report_vi)
        self.assertIn(self.report_vi["text"]["title_design_criteria"], markdown)
        self.assertIn(self.report_vi["text"]["title_final_results"], markdown)
        self.assertIn("qz", markdown.lower())
        self.assertIn("Thư Kudo", markdown)
        self.assertIn("anhthu.phanhuynh219@gmail.com", markdown)

    def test_pdf_generation(self) -> None:
        pdf_bytes = build_pdf(self.report_en)
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))
        self.assertGreater(len(pdf_bytes), 2000)

    def test_copy_blocks_generated(self) -> None:
        blocks = self.report_vi["copy_blocks"]
        for key in ["executive_summary", "input_table", "calculation_breakdown", "final_results", "notes", "author_signature"]:
            self.assertIn(key, blocks)
            self.assertTrue(blocks[key].strip())


if __name__ == "__main__":
    unittest.main()
