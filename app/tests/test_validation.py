from __future__ import annotations

import unittest

from pydantic import ValidationError

from app.domain.schemas import WinLoadInputSchema


class ValidationTests(unittest.TestCase):
    def test_rejects_invalid_wind_zone(self) -> None:
        with self.assertRaises(ValidationError):
            WinLoadInputSchema(wind_zone="V")

    def test_rejects_height_outside_kz_range(self) -> None:
        with self.assertRaises(ValidationError):
            WinLoadInputSchema(eave_height_m=200.0, building_width_m=55.0, roof_slope_percent=10.0)


if __name__ == "__main__":
    unittest.main()
