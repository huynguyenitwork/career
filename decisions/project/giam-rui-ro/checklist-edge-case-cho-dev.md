# checklist edge case cho dev

## mục tiêu
- giúp dev chủ động test rủi ro hệ thống
- giữ ranh giới với qc, không test nghiệp vụ
- dùng được cho api, job, scheduler, service

## nguyên lý cốt lõi
- qc đảm bảo "đúng với người dùng"
- dev đảm bảo "không làm sai khi điều kiện xấu"

---

## nhóm bắt buộc (20% effort → chặn 80% sự cố)

### 1. pre-condition
- thiếu điều kiện → dừng
- không chạy cho có

tiêu chí loại:
- không kiểm soát điều kiện đầu vào → loại

---

### 2. dữ liệu xấu / thiếu
- null
- thiếu field quan trọng
- giá trị bất thường

tiêu chí loại:
- giả định dữ liệu luôn đúng → loại

---

### 3. retry / re-run
- chạy lại job
- gọi lại api

yêu cầu:
- không xử lý trùng
- không nhân đôi dữ liệu

tiêu chí loại:
- chạy lại tạo thêm hiệu ứng → loại

---

### 4. hệ thống khác không phản hồi
- timeout
- lỗi
- không trả dữ liệu

yêu cầu:
- không báo thành công giả
- không xử lý tiếp bừa

---

### 5. fail có kiểm soát
- dừng đúng chỗ
- không sập toàn luồng
- có log, có trạng thái

tiêu chí loại:
- lỗi xảy ra nhưng không biết → loại

---

## nhóm tùy chọn (áp dụng khi rủi ro cao)

### 6. thời điểm & thứ tự
- chạy sớm
- chạy trễ

áp dụng:
- scheduler
- event-driven

---

### 7. chạy song song
- hai job
- hai request cùng dữ liệu

nguy cơ:
- ghi đè
- lệch trạng thái

---

### 8. mất kết nối tạm thời
- gửi nửa chừng
- mạng chập chờn

yêu cầu:
- không mất dữ liệu
- không xử lý nửa vời

---

### 9. báo thành công sớm
- completed khi downstream chưa xong
- lưu trạng thái sai thời điểm

---

### 10. im lặng
- lỗi không log
- skip không dấu vết

yêu cầu:
- log tối thiểu
- truy vết được

---

## bảng quyết định nhanh

- có job / scheduler → test 1–5
- có gọi hệ thống khác → test 1–5
- có retry / chạy lại → test 1–5
- nhiều bước / song song → thêm 6–10
- liên quan tiền / dữ liệu quan trọng → rất nên có 6–10

---

## kết luận
- qc giữ đúng nghiệp vụ
- dev giữ an toàn hệ thống
- checklist dùng để đi trước sự cố, không test cho đủ

làm đúng 20/80:
- ít test hơn
- đúng chỗ hơn
- quyết định nhanh hơn
- production không dạy bài lúc nửa đêm
