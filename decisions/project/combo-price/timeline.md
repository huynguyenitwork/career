## timeline test & sync ecom – rk7 – skytransfer

### mục tiêu
- xác nhận luồng sync store / product / combo chạy đúng với data thật
- khóa phạm vi code + data để test, debug, chuẩn bị release
- giảm rủi ro nghiệp vụ trước khi bàn giao

---

### giai đoạn 1 — dựng khung & webhook (25/11/2025)
- dựng pipeline webhook + service lõi
- chuẩn hóa entity theo yêu cầu thực tế
- refactor service sau test vòng đầu
- tiêu chí đạt: webhook nhận được, service xử lý được

---

### giai đoạn 2 — sync data thật (28/11/2025)
- bổ sung sync combo + update product
- refactor entity + startup do va chạm data thật
- tiêu chí đạt: product + combo sync được từ rk7

---

### giai đoạn 3 — ổn định nhánh & chuẩn hóa (02/12/2025)
- gom nhánh code chung
- khóa cấu trúc chính trước khi add log
- tiêu chí đạt: không còn thay đổi lớn về schema

---

### giai đoạn 4 — quan sát & log (08/12/2025)
- bổ sung log cho ecomservices
- refactor nhẹ để dễ monitor / debug
- tiêu chí đạt: trace được lỗi khi sync

---

### giai đoạn 5 — khoanh vùng & hiểu nghiệp vụ (10–11/12/2025)
- xác định api trung gian: taptap → ecomcontroller → rk7services
- khoanh phạm vi code sử dụng lại
- đọc code cũ + code hiện tại để hiểu luồng combo
- vẽ sơ đồ luồng business do thiếu tài liệu
- đẩy test rủi ro nghiệp vụ
- tiêu chí đạt: hiểu combo hoạt động thế nào, sale data hình thành ra sao

---

### giai đoạn 6 — test store sync (luồng kỹ thuật tối thiểu)
- gọi api store-sync (event: created)
- kiểm tra ghi nhận tại db skytransfer.ecomstore
- tiêu chí đạt: store tạo đúng, status đúng

---

### giai đoạn 7 — test data combo / product (db-level)
- kiểm tra combo: combo, group, product, variant, time, excluded date
- kiểm tra product: product, variant, option
- dùng select để đối soát, delete để làm sạch data test
- tiêu chí đạt: không sót bản ghi phụ thuộc

---

### giai đoạn 8 — mapping dữ liệu rk7 ↔ ecom
- combo: gensapcode (rk7) ↔ combosku (ecom)
- item: gensapcode (rk7) ↔ variantsku (ecom)
- đối chiếu data rk7 và data ecom để phát hiện lệch mapping
- tiêu chí đạt: sku khớp, không sinh combo/item sai

---

### giai đoạn 9 — store procedure phục vụ sync
- sp_ecomvariant: lấy variant chưa xử lý
- sp_ecomcombo: lấy combo chưa xử lý
- sp_ecomcombovariant: map combo ↔ variant
- tiêu chí đạt: sp trả đúng tập dữ liệu cần sync

---

### kết luận nhanh
- đầu sprint: làm cho chạy
- giữa sprint: làm cho đúng data thật
- cuối sprint: làm cho quan sát được
- rủi ro chính: combo + mapping sku
- điểm khóa release: log + store procedure ổn định
