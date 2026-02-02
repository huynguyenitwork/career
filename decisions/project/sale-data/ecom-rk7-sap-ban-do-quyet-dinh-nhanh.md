# ecom - rk7 - sap: bản đồ quyết định nhanh

## 1. khóa nguồn sự thật trước khi làm
- brand có ecom → master data theo ecom → rk7
- brand không có ecom → master data theo sap → ecom → rk7
- sai nguồn sự thật → dừng ngay

## 2. khóa sale data (chỉ 1 luồng)
- sale data luôn đi: rk7 → ecom → sap
- ecom hoặc sap tạo doanh thu → sai → loại
- order có 2 chiều:
  - ecom → rk7 để bán
  - rk7 → ecom để cập nhật & báo cáo

## 3. quyết định nhanh theo loại task
- store / product / menu / price → master data
- order / receipt / daily sales → sale data
- voucher / promotion → gọi ecom để check / redeem
- không phân loại được → chưa hiểu bài toán → dừng

## 4. công thức hiểu hệ thống trong 10 phút
- hệ nào là nguồn? → ghi 1 dòng
- dữ liệu đi từ đâu → về đâu? → vẽ 1 mũi tên
- rk7 có tạo doanh thu không? → có → sale data
- có hơn 2 mũi tên → đang nhiễu → cắt

---

# checklist hỗ trợ dev - hành động ngay

## giai đoạn 1: tiếp cận (≤ 90 phút)
- hỏi dev đang kẹt ở bước nào
- hỏi thiếu thông tin gì để tiếp tục
- hỏi test case nào cần có để unblock
- mở doc → rút ra:
  - luồng chính
  - api cần gọi
  - input / output
- ghi note 1 trang → đủ để dev code

## giai đoạn 2: làm rõ (≤ 1 ngày)
- với ecom:
  - api có sẵn chưa
  - payload đúng chưa
  - auth / whitelist thế nào
- với rk7:
  - mapping field nào
  - inbound api yêu cầu gì
- với sap (nếu có):
  - format
  - field bắt buộc
  - tần suất
- vẽ lại flow 1 trang → dư → xóa
- chốt danh sách test case sống còn

## giai đoạn 3: thực thi (2-3 ngày)
- cung cấp payload test hoàn chỉnh
- mock data nếu hệ ngoài chưa sẵn
- giải thích nghiệp vụ đúng 1 nghĩa
- theo dõi tiến độ → có blocker → gỡ ngay
- chuẩn hóa test case + expected result

## giai đoạn 4: kiểm tra & đóng
- master data:
  - payload đúng nguồn
  - rk7 update đúng
  - không duplicate
  - có log
- sale data:
  - order ecom → rk7 đủ field
  - receipt rk7 → ecom → sap không mất
- xong task:
  - chốt flow
  - chốt payload
  - chốt mapping
  - lưu postman + quickstart

---

# timeline tham gia nhanh (7 ngày)
- day 1: nắm 80% luồng
- day 2: khóa toàn bộ unclear
- day 3: payload + mapping + test case
- day 4: test nội bộ
- day 5: fix + retest
- day 6: e2e test
- day 7: tổng hợp + nghiệm thu

---

# bộ lọc nhiễu khi làm việc
- không ảnh hưởng quyết định hiện tại → loại
- không unblock dev trong 1-2 ngày → loại
- không xác định nguồn dữ liệu → dừng
- nói chung chung, không chỉ ra luồng → dừng

---

# giao tiếp ngang vai senior
- nói thẳng vào luồng và điểm kẹt
- không dùng lý do cá nhân
- nêu rõ đang hỗ trợ theo yêu cầu pm
- tập trung: thiếu gì → cần gì → để làm tiếp