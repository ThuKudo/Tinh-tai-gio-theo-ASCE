from __future__ import annotations

from typing import Any


FORM_SECTIONS: list[dict[str, Any]] = [
    {
        "id": "project",
        "title": {"vi": "Dự án / Thông tin chung", "en": "Project / General info"},
        "description": {
            "vi": "Thông tin nhận diện và lựa chọn tiêu chuẩn tính.",
            "en": "Administrative information and code selection for the check.",
        },
        "fields": [
            {
                "name": "project_name",
                "label": {"vi": "Tên dự án", "en": "Project name"},
                "type": "text",
                "placeholder": {"vi": "Nhà kho Khung A", "en": "Warehouse Frame A"},
                "helper": {
                    "vi": "Dùng cho tiêu đề báo cáo và file xuất.",
                    "en": "Used in exports and report headers.",
                },
            },
            {
                "name": "project_reference",
                "label": {"vi": "Mã tham chiếu", "en": "Project reference"},
                "type": "text",
                "placeholder": {"vi": "WL-ASCE-001", "en": "WL-ASCE-001"},
                "helper": {
                    "vi": "Mã bản vẽ hoặc mã tính toán.",
                    "en": "Short identifier for drawing set or calculation note.",
                },
            },
            {
                "name": "design_code",
                "label": {"vi": "Tiêu chuẩn thiết kế", "en": "Design code"},
                "type": "select",
                "options": ["ASCE 7-10", "ASCE 7-16"],
                "helper": {
                    "vi": "Điều khiển công thức chuyển đổi chu kỳ lặp.",
                    "en": "Controls the return-period conversion formula used by the calculation engine.",
                },
            },
            {
                "name": "building_category",
                "label": {"vi": "Cấp công trình", "en": "Building category"},
                "type": "select",
                "options": ["I", "II", "III", "IV"],
                "helper": {
                    "vi": "Giữ lại cho hồ sơ kiểm tra; mô hình hiện tại chưa dùng trực tiếp trong công thức.",
                    "en": "Retained for audit trail. The current model does not reference it directly in the formulas.",
                },
            },
        ],
    },
    {
        "id": "geometry",
        "title": {"vi": "Hình học / Kích thước", "en": "Geometry / Dimensions"},
        "description": {
            "vi": "Thông số hình học chính chi phối cao độ giữa mái và line load.",
            "en": "Primary geometry driving mean roof height and line-load conversion.",
        },
        "fields": [
            {
                "name": "bay_spacing_m",
                "label": {"vi": "Bước khung", "en": "Bay spacing"},
                "type": "number",
                "step": "0.1",
                "unit": "m",
                "placeholder": {"vi": "1.0", "en": "1.0"},
                "helper": {
                    "vi": "Dùng làm hệ số nhân để đổi áp lực sang line load.",
                    "en": "Used as the multiplier for line-load labels.",
                },
            },
            {
                "name": "eave_height_m",
                "label": {"vi": "Cao giọt nước H", "en": "Eave height H"},
                "type": "number",
                "step": "0.1",
                "unit": "m",
                "placeholder": {"vi": "23.0", "en": "23.0"},
                "helper": {
                    "vi": "Phải nằm trong miền bảng nội suy Kz.",
                    "en": "Must remain within the Kz table height range.",
                },
            },
            {
                "name": "roof_slope_percent",
                "label": {"vi": "Độ dốc mái i", "en": "Roof slope i"},
                "type": "number",
                "step": "0.1",
                "unit": "%",
                "placeholder": {"vi": "10.0", "en": "10.0"},
                "helper": {
                    "vi": "Được đổi sang góc mái theo atan(i/100).",
                    "en": "Converted to roof angle using atan(i/100).",
                },
            },
            {
                "name": "building_width_m",
                "label": {"vi": "Bề rộng nhà Bf", "en": "Building width Bf"},
                "type": "number",
                "step": "0.1",
                "unit": "m",
                "placeholder": {"vi": "55.0", "en": "55.0"},
                "helper": {
                    "vi": "Tham gia công thức tính cao độ giữa mái.",
                    "en": "Used in mean roof height calculation.",
                },
            },
            {
                "name": "building_length_m",
                "label": {"vi": "Chiều dài nhà Lf", "en": "Building length Lf"},
                "type": "number",
                "step": "0.1",
                "unit": "m",
                "placeholder": {"vi": "61.8", "en": "61.8"},
                "helper": {
                    "vi": "Giữ để mô tả hình học; mô hình hiện tại chưa sử dụng trong công thức.",
                    "en": "Preserved for geometry context; not used by the current model formulas.",
                },
            },
        ],
    },
    {
        "id": "wind",
        "title": {"vi": "Thông số gió", "en": "Wind parameters"},
        "description": {
            "vi": "Vùng gió và các chu kỳ lặp dùng trong mô hình tính.",
            "en": "Wind zone and return-period parameters used by the calculation model.",
        },
        "fields": [
            {
                "name": "wind_zone",
                "label": {"vi": "Vùng gió", "en": "Wind zone"},
                "type": "select",
                "options": ["I", "II", "III", "IV"],
                "helper": {
                    "vi": "Ánh xạ trực tiếp sang áp lực gió cơ bản W0.",
                    "en": "Maps directly to QCVN base pressure W0.",
                },
            },
            {
                "name": "source_return_period_years",
                "label": {"vi": "Chu kỳ lặp nguồn", "en": "Source return period"},
                "type": "number",
                "step": "1",
                "unit": "years",
                "placeholder": {"vi": "50", "en": "50"},
                "helper": {
                    "vi": "Chu kỳ lặp nguồn dùng cho bước chuyển đổi vận tốc.",
                    "en": "Source return period used in the speed conversion step.",
                },
            },
            {
                "name": "target_return_period_years",
                "label": {"vi": "Chu kỳ lặp mục tiêu", "en": "Target return period"},
                "type": "number",
                "step": "1",
                "unit": "years",
                "placeholder": {"vi": "1700", "en": "1700"},
                "helper": {
                    "vi": "Chu kỳ lặp mục tiêu dùng để xác định vận tốc thiết kế.",
                    "en": "Target return period used to determine the design wind speed.",
                },
            },
            {
                "name": "qcvn_reference_years",
                "label": {"vi": "Chu kỳ tham chiếu QCVN", "en": "QCVN reference period"},
                "type": "number",
                "step": "1",
                "unit": "years",
                "placeholder": {"vi": "20", "en": "20"},
                "helper": {
                    "vi": "Ô AF12 dùng để đổi V20 sang V50.",
                    "en": "Reference period used to convert V20 to V50.",
                },
            },
        ],
    },
    {
        "id": "exposure",
        "title": {"vi": "Địa hình / Nội áp", "en": "Exposure / Internal pressure"},
        "description": {
            "vi": "Chọn dạng địa hình và kiểu bao che để xác định Kz, GCpi.",
            "en": "Exposure class and enclosure assumptions driving Kz and GCpi.",
        },
        "fields": [
            {
                "name": "exposure_category",
                "label": {"vi": "Dạng địa hình", "en": "Exposure category"},
                "type": "select",
                "options": ["B", "C", "D"],
                "helper": {
                    "vi": "Chọn cột nội suy trong bảng Kz.",
                    "en": "Selects the interpolation column from the Kz table.",
                },
            },
            {
                "name": "enclosure_type",
                "label": {"vi": "Kiểu bao che", "en": "Enclosure classification"},
                "type": "select",
                "options": ["Open", "Partially Enclosed", "Enclosed"],
                "helper": {
                    "vi": "Quy định GCpi và việc triệt tiêu một số áp lực tường của nhà hở.",
                    "en": "Controls GCpi and zeroes some wall pressures for open buildings.",
                },
            },
        ],
    },
    {
        "id": "advanced",
        "title": {"vi": "Tùy chọn nâng cao / Override", "en": "Advanced options / Overrides"},
        "description": {
            "vi": "Cho phép thay đổi các hằng số mặc định của mô hình.",
            "en": "Optional overrides for the default model constants.",
        },
        "fields": [
            {
                "name": "topographic_factor",
                "label": {"vi": "Hệ số địa hình Kzt", "en": "Topographic factor Kzt"},
                "type": "number",
                "step": "0.01",
                "unit": "-",
                "placeholder": {"vi": "1.00", "en": "1.00"},
                "helper": {
                    "vi": "Giá trị mặc định của mô hình là 1.00.",
                    "en": "The default model value is 1.00.",
                },
            },
            {
                "name": "wind_directionality_factor",
                "label": {"vi": "Hệ số hướng gió Kd", "en": "Directionality factor Kd"},
                "type": "number",
                "step": "0.01",
                "unit": "-",
                "placeholder": {"vi": "0.85", "en": "0.85"},
                "helper": {
                    "vi": "Giá trị mặc định của mô hình là 0.85.",
                    "en": "The default model value is 0.85.",
                },
            },
        ],
    },
]


APP_ASSUMPTIONS = {
    "vi": [
        "Calculation engine áp dụng nhất quán bộ công thức và bảng tham chiếu của mô hình tính tải gió.",
        "Cấp công trình được giữ lại cho hồ sơ, nhưng mô hình hiện tại chưa tham chiếu trực tiếp trong công thức.",
        "Các giá trị Kz và GCpf được nội suy tuyến tính từ các bảng tham chiếu nội bộ.",
        "Bảng góc mái chỉ có hiệu lực trong miền 0 đến 90 độ.",
        "Nhãn line load được format nhất quán theo quy tắc làm tròn một chữ số thập phân.",
    ],
    "en": [
        "The calculation engine applies a consistent set of wind load formulas and reference tables.",
        "Building category is retained for documentation, although the current model formulas do not reference it directly.",
        "Kz and GCpf values are obtained by linear interpolation from the internal reference tables.",
        "The roof-angle table is valid for the domain 0 to 90 degrees.",
        "Line-load labels follow a consistent one-decimal rounding rule.",
    ],
}
