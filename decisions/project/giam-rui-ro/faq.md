# xử lý nền, queue, state machine 

mục tiêu:
- dùng để quyết định thiết kế job / worker trong 7–30 ngày
- giảm lỗi im lặng, giảm retry mù, giảm phụ thuộc ngầm
- chọn đúng công cụ → đi nhanh đủ đúng

---

## timeline vấn đề (từ lúc code → lúc vận hành)

### t0 — bắt đầu code job
- dùng ef + savechanges cho mọi update
- giả định ef luôn update nếu không lỗi
- **rủi ro**: ef phụ thuộc changetracker

### t1 — job chạy nền
- nhiều dbcontext
- update trạng thái theo bước
- không reload entity
- **hệ quả**: ef thiếu thông tin state

### t2 — savechanges im lặng
- không exception
- 0 row affected
- trạng thái không đổi
- **hệ quả**: job kẹt, retry vô nghĩa

### t3 — vận hành phát hiện muộn
- pending tăng
- processing treo lâu
- failed không rõ nguyên nhân
- **chi phí**: debug, can thiệp tay

---

## nguyên nhân cốt lõi (chỉ giữ thứ ảnh hưởng quyết định)

- savechanges phụ thuộc:
  - entity phải được track
  - biết giá trị cũ
  - không xung đột concurrency
- job / worker vi phạm cả 3
- **kết luận**: sai ngữ cảnh sử dụng

---

## quyết định kỹ thuật đúng

### dùng savechanges khi
- crud / api / form
- 1 dbcontext
- entity sống xuyên suốt request
- **tiêu chí loại**: job nền → loại

### dùng executesqlcommand khi
- update trạng thái
- state machine
- nhiều dbcontext
- db là source of truth
- cần biết row affected
- **kết luận**: chọn ngay
**lưu ý**: không sử dụng hàm **asnotracking** với dbset nếu update
---

## chuẩn hóa state machine (tối thiểu)

- pending: có việc, chưa xử
- processing: đang xử
- done: xong
- failed: không xong

**loại bỏ**:
- trạng thái để “chờ nhau”
- trạng thái mơ hồ không dùng cho quyết định

---

## queue — bản chất cần nhớ

- queue chỉ giữ việc
- không tạo thứ tự
- worker:
  - không biết job khác
  - chỉ check điều kiện
  - xong thì cập nhật

**kết luận**:
- thứ tự nằm ở logic
- không nằm ở thời gian

---

## retry — dùng khi nào

- lỗi tạm thời
- retry an toàn
- có maxretry

**loại bỏ retry khi**:
- side-effect không quay đầu
- retry gây trùng

---

## timing / delay — không lạm dụng

- dùng để giãn tải
- dùng cho backoff
- không dùng để tạo thứ tự

---

## monitoring — chỉ nhìn 4 số

- pending tăng → tồn
- processing lâu → treo
- failed nhiều → lỗi hệ thống
- retry tăng đều → điều kiện chưa tới

**loại bỏ**:
- soi từng job
- log không dẫn hành động

---

## auto-healing — tiêu chuẩn sống còn

- worker stateless
- job nằm trong db
- worker chết → job còn
- retry tự chạy

**kết luận**:
- hệ thống không cần anh hùng
- chỉ cần không quên việc

---

## bảng ưu tiên điều phối (chốt thiết kế)

### ưu tiên 1 — bắt buộc
- 1 job = 1 entity
- có status trong db
- idempotent
- check điều kiện trong handler
- worker stateless

### ưu tiên 2 — làm sớm
- retry giới hạn
- song song có kiểm soát
- lock tránh trùng
- dashboard 4 số

### ưu tiên 3 — để sau
- delay / backoff
- priority
- dead letter

---

## 3 câu khóa não (đủ dùng)

- queue không tạo thứ tự, chỉ giữ việc
- thứ tự nằm trong điều kiện, không nằm trong thời gian
- làm đúng trước, tối ưu sau
