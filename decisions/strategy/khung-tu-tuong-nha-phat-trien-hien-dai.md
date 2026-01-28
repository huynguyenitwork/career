# timeline

- [28-01-2026] khung tư tưởng nhà phát triển hiện đại

---

# khung tư tưởng nhà phát triển hiện đại
mục tiêu: ra quyết định nhanh, loại nhiễu sớm, đi thẳng vào thay đổi tạo lợi thế

---

## 1. timeline lịch sử tiến bộ khoa học – kỹ thuật (các bước ngoặt còn hiệu lực)

### 1940–1960 | tư duy thuật toán
- vấn đề: máy hiếm, lỗi = thảm họa
- khởi xướng: von neumann, turing
- đóng góp: tư duy tuần tự, giả định rõ
- giới hạn: không scale theo độ phức tạp

### 1968–1980 | kiểm soát độ phức tạp
- vấn đề: phần mềm vượt khả năng não người
- khởi xướng: dijkstra, wirth
- đóng góp: chia nhỏ, kiểm soát luồng
- giới hạn: chưa xử lý được thay đổi domain

### 1980–1995 | mô hình hóa domain
- vấn đề: sửa nhỏ vỡ lớn
- khởi xướng: booch, stroustrup
- đóng góp: encapsulation, trách nhiệm rõ
- giới hạn: bị lạm dụng kỹ thuật oop

### 1995–2005 | phản hồi nhanh
- vấn đề: dự án chết vì con người
- khởi xướng: kent beck, fowler
- đóng góp: agile, tdd
- giới hạn: chưa đủ cho hệ phân tán

### 2005–2015 | hệ phân tán
- vấn đề: không thể đúng tuyệt đối
- khởi xướng: eric evans, google
- đóng góp: ddd, eventual consistency
- giới hạn: hệ quá phức tạp để hiểu bằng đầu

### 2015–nay | quan sát & quyết định
- vấn đề: debug truyền thống vô dụng
- khởi xướng: charity majors, gene kim
- đóng góp: observability, devops
- trạng thái hiện tại: developer = người ra quyết định hệ thống

---

## 2. di sản còn hiệu lực & cách thích ứng linh hoạt

### tư duy tuần tự
- giữ: giả định rõ, input/output rõ
- dùng khi: core logic
- bỏ khi: mô hình toàn hệ động

### chia nhỏ & kiểm soát
- giữ: giảm tải nhận thức
- dùng khi: hàm, module
- bỏ khi: ép cấu trúc cứng cho domain thay đổi nhanh

### mô hình domain
- giữ: code phản ánh thực tế
- dùng khi: business logic
- bỏ: inheritance phức tạp, entity kỹ thuật

### phản hồi nhanh
- giữ: sai sớm để sửa sớm
- dùng khi: quyết định có thể đảo ngược
- bỏ: ceremony hình thức

### chấp nhận sai
- giữ: hệ phải chịu lỗi
- dùng khi: distributed system
- bỏ: cố đồng bộ tuyệt đối

### quan sát được
- giữ: thấy mới quyết
- dùng khi: production, sự cố
- bỏ: log để an tâm

---

## 3. bộ công cụ ra quyết định nhanh (dùng hàng ngày)

### goal lock
- viết 1 dòng: "quyết định 7–30 ngày là gì?"
- không trả lời được → loại task

### payoff filter
- chọn 1 việc tạo thay đổi lớn nhất
- không ảnh hưởng 7–30 ngày → loại

### assumption lock
- ghi 3 giả định chính (data, timing, load)
- không kiểm chứng được → không build quanh nó

### boundary cut
- mỗi module trả lời: nhận gì / trả gì
- phụ thuộc ngầm → cắt

### noise killer
- hỏi: "thông tin này dùng để làm gì?"
- không đổi hành động → loại

### fast enough rule
- ưu tiên quyết định đảo ngược được
- chờ hoàn hảo → chậm

### externalize não
- ghi hết ra note
- khóa 1 luồng chính

### decision review
- mỗi quyết định ghi:
  - quyết định
  - giả định đúng/sai
  - rule rút ra

---

## 4. ví dụ xuyên suốt: discount không persist (staging)

### goal lock
- mục tiêu: xác định nguyên nhân và chặn tái diễn
- loại: refactor, tối ưu, bàn kiến trúc dài hạn

### payoff filter
- chọn: thêm log + trace
- loại: đọc hết code, viết lại module

### assumption lock
- giả định:
  - persist được gọi
  - transaction commit
  - ghi đúng boundary
- mỗi giả định = 1 log

### boundary cut
- skytransfer gửi intent
- skycrm chịu trách nhiệm persist
- kiểm tra service nào ghi db

### noise killer
- loại: "chắc cache", "chắc db lag"
- chỉ tin log + trace

### fast enough rule
- phát hiện exception bị swallow
- quyết định: fail fast + log
- không refactor lớn

### externalize não
- ghi giả định, kết quả log, bước tiếp theo
- khóa 1 luồng: theo trace đến commit

### decision review
- rule rút ra:
  - persist quan trọng phải log tại commit point
- thêm checklist cho lần sau

---

## kết luận cốt lõi
- đi xa không phải vì biết thêm
- mà vì dùng đúng di sản, đúng thời điểm
- lợi thế hiện đại:
  - loại sớm
  - quyết định sớm
  - học trực tiếp từ hệ thống

