# Win Load ASCE App

Ứng dụng web Python thay thế workflow Excel của sheet `Win Load ASCE`, với calculation engine đã kiểm chứng, giao diện song ngữ Việt/Anh, và hệ xuất báo cáo kỹ thuật HTML/Markdown/PDF.

## Điểm chính

- Giữ nguyên logic tính toán đã reverse-engineer từ workbook.
- Giao diện song ngữ:
  - Mặc định `Tiếng Việt`
  - Chuyển sang `English` ngay trên UI
- Chức năng report production-ready:
  - HTML report in đẹp
  - Markdown copy-friendly
  - PDF export trực tiếp
  - Copy-ready blocks cho:
    - Executive Summary
    - Input Table
    - Calculation Breakdown
    - Final Results
    - Notes

## Stack

- `FastAPI`: API thật, validation typed, dễ test tích hợp.
- `Jinja2 + HTML/CSS/JS`: UI sạch, responsive, không cần Node build chain.
- `reportlab`: xuất PDF trực tiếp từ Python.

## Cấu trúc project

```text
win_load_asce_app/
|-- app/
|   |-- domain/
|   |   |-- config.py
|   |   |-- formulas.py
|   |   |-- models.py
|   |   |-- reporting.py
|   |   |-- schemas.py
|   |   `-- service.py
|   |-- reporting/
|   |   |-- localization.py
|   |   |-- pdf_export.py
|   |   `-- report_builder.py
|   |-- tests/
|   |   |-- test_api.py
|   |   |-- test_engine.py
|   |   |-- test_legacy_core.py
|   |   |-- test_report.py
|   |   `-- test_validation.py
|   |-- web/
|   |   |-- static/
|   |   |   |-- css/styles.css
|   |   |   `-- js/app.js
|   |   `-- templates/
|   |       |-- index.html
|   |       `-- report.html
|   |-- __init__.py
|   `-- main.py
|-- docs/ui_overview.md
|-- sample_data/default_input.json
|-- sample_reports/
|-- build_exe.bat
|-- desktop_launcher.py
|-- generate_sample_reports.py
|-- requirements.txt
`-- run.py
```

## Cài đặt

```powershell
cd "D:\03. LEARNING\0. Python\win_load_asce_app"
..\venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Chạy app

```powershell
cd "D:\03. LEARNING\0. Python\win_load_asce_app"
..\venv\Scripts\python.exe run.py
```

Mở `http://127.0.0.1:8000`.

## Chạy test

```powershell
cd "D:\03. LEARNING\0. Python\win_load_asce_app"
$env:PYTHONPATH = (Get-Location).Path
..\venv\Scripts\python.exe -m unittest discover -s app/tests -v
```

## Xuất báo cáo

Trong giao diện, sau khi chạy tính:

- `Xuất HTML`
- `Xuất Markdown`
- `Xuất PDF`
- `Copy tóm tắt`
- `Copy bảng input`
- `Copy diễn giải tính`
- `Copy kết quả cuối`

Report được sinh từ dữ liệu thực của engine, gồm:

- Thông tin dự án
- Calculation summary
- Design criteria / code references
- Input parameters
- Assumptions
- Intermediate calculations
- Final results
- Notes / warnings / limitations

## Sinh sample reports

```powershell
cd "D:\03. LEARNING\0. Python\win_load_asce_app"
$env:PYTHONPATH = (Get-Location).Path
..\venv\Scripts\python.exe generate_sample_reports.py
```

Kết quả mẫu nằm trong:

- [sample_report_vi.html](./sample_reports/sample_report_vi.html)
- [sample_report_vi.md](./sample_reports/sample_report_vi.md)
- [sample_report_vi.pdf](./sample_reports/sample_report_vi.pdf)
- [sample_report_en.html](./sample_reports/sample_report_en.html)
- [sample_report_en.md](./sample_reports/sample_report_en.md)
- [sample_report_en.pdf](./sample_reports/sample_report_en.pdf)

## Kiểm chứng

- Parity với workbook cũ: có
- Parity với Python core trước đó: có
- Test validation: có
- Test API/report export: có
- Test report builder/PDF/Markdown/copy blocks: có

## Ghi chú

- `building_category` và `building_length_m` vẫn được giữ trong app để phục vụ hồ sơ và mở rộng về sau, dù workbook hiện chưa dùng trực tiếp trong công thức.
- PDF hiện được render bằng `reportlab`, không phụ thuộc Excel hoặc trình duyệt ngoài.
- Nếu cần build `.exe`, dùng `build_exe.bat` sau khi kiểm tra app web đã ổn.
