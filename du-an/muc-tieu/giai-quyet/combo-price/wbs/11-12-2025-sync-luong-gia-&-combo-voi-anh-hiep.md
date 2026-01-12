# wbs 20/80 cho task 11-12-2025 – sync luồng giá & combo (người mới)
Rồi, gom gọn theo đúng tinh thần **20/80**: chỉ giữ 20% hành động tạo ra 80% kết quả để bạn kịp chạy nước rút trước go-live.

---

## 20/80 – Phần bạn cần xử lý ngay (phiên bản siêu ngắn gọn, dễ hành động)

**1) Hiểu combo đang chạy như thế nào (AS-IS).**
Đây là 20% hiểu biết nền tảng nhưng quyết định 80% khả năng bạn test được.
– Mở code phần xử lý combo → nắm luồng input → xử lý → output sang RK7.
– Xác định những điểm quan trọng: mapping combo – item, tính giá combo vs giá lẻ.

**2) Kiểm tra combo trực tiếp trên RK7.**
Đây là nơi xác thực thực tế, không đoán mò.
– Mở 1 combo thật trong RK7 → xem cấu trúc, child items, logic giá.
– So sánh với dữ liệu code đang gửi.

**3) Sync nhanh với anh Hiệp.**
10–15 phút đủ để cắt 80% thời gian tự mò.
– Hỏi combo nào đang dùng để test.
– Hỏi luồng combo hiện tại có gì đặc biệt (đã từng xử lý trước đó).

**4) Test thử một combo mẫu, không chờ structure final.**
Mục tiêu là nắm quy tắc vận hành, không phải test chính xác dữ liệu final.
– Dùng combo mẫu trong code hoặc trên RK7 để bắn thử request.
– Bắt log → hiểu server phản hồi ra sao → có cơ sở fix nhanh.

---

## Kết quả mong đợi khi bạn hoàn thành 4 bước trên

– Bạn hiểu được combo hiện tại (đủ để test, không cần hoàn hảo).
– Bạn test được giá combo vs giá lẻ.
– Bạn phối hợp với anh Hiệp đúng trọng tâm.
– Bạn không bị “mù” khi structure final từ đối tác được gửi đến.

---

Nếu bạn muốn, mình có thể viết thêm bản để bạn gửi lại cho PO theo kiểu báo cáo tiến độ, ngắn – rõ – dứt khoát.

