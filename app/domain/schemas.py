from __future__ import annotations

from pydantic import BaseModel, Field, field_validator, model_validator


class WinLoadInputSchema(BaseModel):
    project_name: str = Field(default="Default ASCE Wind Check", max_length=120)
    project_reference: str = Field(default="WL-ASCE-001", max_length=60)
    design_code: str = Field(default="ASCE 7-16")
    wind_zone: str = Field(default="IV")
    exposure_category: str = Field(default="B")
    building_category: str = Field(default="III")
    bay_spacing_m: float = Field(default=1.0, gt=0)
    eave_height_m: float = Field(default=23.0, gt=0)
    roof_slope_percent: float = Field(default=10.0, ge=0, le=200)
    building_width_m: float = Field(default=55.0, gt=0)
    building_length_m: float = Field(default=61.8, gt=0)
    enclosure_type: str = Field(default="Enclosed")
    source_return_period_years: float = Field(default=50.0, gt=0)
    target_return_period_years: float = Field(default=1700.0, gt=0)
    qcvn_reference_years: float = Field(default=20.0, gt=0)
    topographic_factor: float = Field(default=1.0, gt=0)
    wind_directionality_factor: float = Field(default=0.85, gt=0)

    @field_validator("design_code")
    @classmethod
    def validate_design_code(cls, value: str) -> str:
        allowed = {"ASCE 7-10", "ASCE 7-16"}
        if value not in allowed:
            raise ValueError(f"Design code must be one of {sorted(allowed)}.")
        return value

    @field_validator("wind_zone")
    @classmethod
    def validate_wind_zone(cls, value: str) -> str:
        allowed = {"I", "II", "III", "IV"}
        if value not in allowed:
            raise ValueError(f"Wind zone must be one of {sorted(allowed)}.")
        return value

    @field_validator("exposure_category")
    @classmethod
    def validate_exposure(cls, value: str) -> str:
        allowed = {"B", "C", "D"}
        if value not in allowed:
            raise ValueError(f"Exposure category must be one of {sorted(allowed)}.")
        return value

    @field_validator("building_category")
    @classmethod
    def validate_building_category(cls, value: str) -> str:
        allowed = {"I", "II", "III", "IV"}
        if value not in allowed:
            raise ValueError(f"Building category must be one of {sorted(allowed)}.")
        return value

    @field_validator("enclosure_type")
    @classmethod
    def validate_enclosure(cls, value: str) -> str:
        allowed = {"Open", "Partially Enclosed", "Enclosed"}
        if value not in allowed:
            raise ValueError(f"Enclosure type must be one of {sorted(allowed)}.")
        return value

    @model_validator(mode="after")
    def validate_geometry(self) -> "WinLoadInputSchema":
        if self.eave_height_m > 152.4:
            raise ValueError("Eave height exceeds the Kz interpolation table range of 152.4 m.")
        if self.mean_roof_height_m > 152.4:
            raise ValueError("Mean roof height exceeds the Kz interpolation table range of 152.4 m.")
        if self.roof_angle_deg > 90:
            raise ValueError("Roof slope results in an angle greater than 90 degrees.")
        return self

    @property
    def roof_angle_deg(self) -> float:
        import math

        return math.degrees(math.atan(self.roof_slope_percent / 100.0))

    @property
    def mean_roof_height_m(self) -> float:
        return self.eave_height_m + 0.25 * self.building_width_m * self.roof_slope_percent / 100.0


class ExportRequestSchema(BaseModel):
    inputs: WinLoadInputSchema
