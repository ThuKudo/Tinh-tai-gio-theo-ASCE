from __future__ import annotations

import sys
import unittest
from pathlib import Path

from app.domain.schemas import WinLoadInputSchema
from app.domain.service import build_response


LEGACY_ROOT = Path(__file__).resolve().parents[3] / "wind_load_app"


class LegacyCoreParityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        sys.path.insert(0, str(LEGACY_ROOT))
        from asce_win_load.main import build_output_payload, default_inputs  # type: ignore

        cls.legacy = build_output_payload(default_inputs())
        cls.current = build_response(WinLoadInputSchema())

    def test_key_values_match_legacy_core(self) -> None:
        self.assertAlmostEqual(self.current["raw"]["design_speed_mps"], self.legacy["design_speed_mps"], places=12)
        self.assertAlmostEqual(self.current["raw"]["qz_kn_per_m2"], self.legacy["qz_kn_per_m2"], places=12)
        self.assertAlmostEqual(self.current["raw"]["case_a_z2"]["wl1_or_we1"], self.legacy["case_a_z2"]["wl1_or_we1"], places=12)
        self.assertAlmostEqual(self.current["raw"]["case_b_z5"]["wl2_or_we2"], self.legacy["case_b_z5"]["wl2_or_we2"], places=12)

    def test_line_load_labels_match_legacy_core(self) -> None:
        self.assertEqual(self.current["outputs"]["line_load_labels"], self.legacy["line_load_labels"])


if __name__ == "__main__":
    unittest.main()
