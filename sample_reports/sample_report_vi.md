# Báo cáo tính toán tải gió ASCE

Dựa trên thông số gió, hệ số nội áp và các giá trị tra bảng tương ứng, áp lực vận tốc thiết kế được xác định và tổ hợp thành các áp lực vùng Case A và Case B phục vụ kiểm tra khung chính và đầu hồi. Áp lực vận tốc qz: 2.517 kN/m². Case A Z2 = -2.189 kN/m².

## Thông tin công trình
- Tên dự án: Bao cao mau
- Mã tham chiếu: WL-VI-001
- Người phụ trách: Thư Kudo - anhthu.phanhuynh219@gmail.com
- Thời điểm sinh báo cáo: 2026-03-10T16:03:49.373985+00:00

## Tiêu chuẩn và tiêu chí thiết kế
Thiết kế sử dụng các công thức chuyển đổi vận tốc gió theo QCVN và ASCE, nội suy hệ số Kz và GCpf theo bảng tham chiếu nội bộ, và tổ hợp nội áp GCpi theo kiểu bao che công trình.

## Thông số đầu vào
| Parameter | Value |
|---|---|
| Tên dự án | Bao cao mau |
| Mã tham chiếu | WL-VI-001 |
| Tiêu chuẩn thiết kế | ASCE 7-16 |
| Vùng gió | IV |
| Dạng địa hình | B |
| Cấp công trình | III |
| Bước khung | 1 m |
| Cao giọt nước H | 23 m |
| Độ dốc mái i | 10 % |
| Bề rộng nhà Bf | 55 m |
| Chiều dài nhà Lf | 61.8 m |
| Kiểu bao che | Enclosed |
| Chu kỳ lặp nguồn | 50 năm |
| Chu kỳ lặp mục tiêu | 1,700 năm |
| Chu kỳ tham chiếu QCVN | 20 năm |
| Hệ số địa hình Kzt | 1 |
| Hệ số hướng gió Kd | 0.85 |

## Giả định
- Calculation engine áp dụng nhất quán bộ công thức và bảng tham chiếu của mô hình tính tải gió.
- Cấp công trình được giữ lại cho hồ sơ, nhưng mô hình hiện tại chưa tham chiếu trực tiếp trong công thức.
- Các giá trị Kz và GCpf được nội suy tuyến tính từ các bảng tham chiếu nội bộ.
- Bảng góc mái chỉ có hiệu lực trong miền 0 đến 90 độ.
- Nhãn line load được format nhất quán theo quy tắc làm tròn một chữ số thập phân.

## Giá trị trung gian
- w0_dan_per_m2: 155.000000
- v20_mps: 50.284671
- v50_mps: 55.375697
- return_period_factor: 1.301629
- design_speed_mps: 72.078621
- design_speed_kph: 259.483034
- design_speed_mph: 161.235258
- roof_angle_deg: 5.710593
- mean_roof_height_m: 24.375000
- kz: 0.929677
- kzt: 1.000000
- kd: 0.850000
- qz_kn_per_m2: 2.516660
- gcpi_positive: 0.180000
- gcpi_negative: -0.180000

## Kết quả cuối cùng
## Kết quả cuối cùng
- Áp lực vận tốc qz: 2.517 kN/m²
- Vận tốc gió thiết kế: 72.079 m/s
- Case A Z1: WL1/WR1 = 0.569, WL2/WR2 = 1.475
- Case A Z2: WL1/WR1 = -2.189, WL2/WR2 = -1.283
- Case A Z3: WL1/WR1 = -1.397, WL2/WR2 = -0.491
- Case A Z4: WL1/WR1 = -1.2, WL2/WR2 = -0.294
- Case B Z1: WE1/WE3 = -1.585, WE2/WE4 = -0.679
- Case B Z2: WE1/WE3 = -2.189, WE2/WE4 = -1.283
- Case B Z3: WE1/WE3 = -1.384, WE2/WE4 = -0.478
- Case B Z4: WE1/WE3 = -1.585, WE2/WE4 = -0.679
- Case B Z5: WE1/WE3 = 0.554, WE2/WE4 = 1.46
- Case B Z6: WE1/WE3 = -1.183, WE2/WE4 = -0.277

## Ghi chú / giới hạn
- Calculation engine áp dụng nhất quán bộ công thức và bảng tham chiếu của mô hình tính tải gió.
- Cấp công trình được giữ lại cho hồ sơ, nhưng mô hình hiện tại chưa tham chiếu trực tiếp trong công thức.
- Các giá trị Kz và GCpf được nội suy tuyến tính từ các bảng tham chiếu nội bộ.
- Bảng góc mái chỉ có hiệu lực trong miền 0 đến 90 độ.
- Nhãn line load được format nhất quán theo quy tắc làm tròn một chữ số thập phân.
- Case A mái đón gió đang chi phối áp lực âm lớn hơn đầu hồi.

Người phụ trách: Thư Kudo - anhthu.phanhuynh219@gmail.com