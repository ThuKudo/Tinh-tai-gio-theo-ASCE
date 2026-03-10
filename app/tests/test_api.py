from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from app.main import app


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def test_form_config_endpoint(self) -> None:
        response = self.client.get("/api/form-config")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("sections", payload)
        self.assertIn("defaults", payload)
        self.assertEqual(payload["default_language"], "vi")

    def test_calculate_endpoint(self) -> None:
        response = self.client.post("/api/calculate?lang=vi", json={"project_name": "API Test"})
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["meta"]["project_name"], "API Test")
        self.assertAlmostEqual(payload["intermediate"]["qz_kn_per_m2"], 2.51666, places=5)
        self.assertEqual(payload["language"], "vi")

    def test_calculate_validation_error(self) -> None:
        response = self.client.post("/api/calculate", json={"wind_zone": "V"})
        self.assertEqual(response.status_code, 422)

    def test_html_report_export(self) -> None:
        response = self.client.post("/api/report/html?lang=en", json={"inputs": {"project_name": "Report Demo"}})
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])
        self.assertIn("Report Demo", response.text)

    def test_markdown_report_export(self) -> None:
        response = self.client.post("/api/report/markdown?lang=vi", json={"inputs": {"project_name": "Bao cao API"}})
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/markdown", response.headers["content-type"])
        self.assertIn("Báo cáo", response.text)

    def test_pdf_report_export(self) -> None:
        response = self.client.post("/api/report/pdf?lang=en", json={"inputs": {"project_name": "PDF API"}})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/pdf")
        self.assertTrue(response.content.startswith(b"%PDF"))

    def test_report_blocks_endpoint(self) -> None:
        response = self.client.post("/api/report/blocks?lang=vi", json={"inputs": {"project_name": "Blocks API"}})
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("blocks", payload)
        self.assertIn("executive_summary", payload["blocks"])


if __name__ == "__main__":
    unittest.main()
