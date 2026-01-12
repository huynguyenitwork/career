# checklist edge case cho dev

## nguyên lý 20/80 – quyết định nhanh, giảm rủi ro hệ thống

### mục tiêu tài liệu

* giúp dev chủ động test các **trường hợp rủi ro hệ thống**
* phân rõ ranh giới với qc (không test lại nghiệp vụ)
* áp dụng được cho **hầu hết mọi hệ thống**: api, job, scheduler, service

nguyên lý cốt lõi:

> qc đảm bảo hệ thống **đúng với người dùng**
> dev đảm bảo hệ thống **không làm sai khi điều kiện không hoàn hảo**

---

## i. nhóm bắt buộc

### 20% effort – chặn 80% sự cố production

các test sau **hệ thống nào cũng cần có**.

---

### 1. pre-condition – đủ điều kiện mới chạy

kiểm tra trước khi xử lý:

* thiếu điều kiện → phải dừng
* không chạy "cho có"

ví dụ:

* store bị disable → skip
* feature flag tắt → không chạy chui

---

### 2. dữ liệu xấu / dữ liệu thiếu

hệ thống phải xử lý an toàn khi:

* dữ liệu null
* thiếu field quan trọng
* giá trị bất thường

ví dụ:

* giá = 0
* id không tồn tại

---

### 3. chạy lại có an toàn không (retry / re-run)

kiểm tra:

* job chạy lại
* api gọi lại

yêu cầu:

* không xử lý trùng
* không nhân đôi dữ liệu

---

### 4. hệ thống khác không phản hồi

tình huống:

* timeout
* không trả lời
* trả lỗi

yêu cầu:

* không báo thành công giả
* không làm tiếp bừa

---

### 5. fail có kiểm soát

khi lỗi xảy ra:

* dừng đúng chỗ
* không làm sập toàn bộ luồng
* có log, có trạng thái rõ

---

## ii. nhóm tùy chọn

### test thêm để giảm rủi ro với hệ thống quan trọng

không bắt buộc cho mọi hệ thống, nhưng **nên có khi rủi ro cao**.

---

### 6. thứ tự & thời điểm

kiểm tra:

* chạy sớm hơn dự kiến
* chạy trễ hơn dự kiến

áp dụng cho:

* scheduler
* event-driven system

---

### 7. chạy song song

tình huống:

* hai job xử lý cùng một dữ liệu
* hai request cùng lúc

nguy cơ:

* ghi đè
* dữ liệu không nhất quán

---

### 8. mất kết nối tạm thời

tình huống:

* mạng chập chờn
* gửi được nửa chừng

yêu cầu:

* không mất dữ liệu
* không xử lý nửa vời

---

### 9. báo "thành công" quá sớm

kiểm tra:

* đánh dấu completed khi downstream chưa xong
* lưu trạng thái sai thời điểm

áp dụng:

* job nhiều bước
* có hệ thống phụ thuộc

---

### 10. im lặng

tình huống:

* lỗi xảy ra nhưng không ai biết
* job skip mà không có dấu vết

yêu cầu:

* log tối thiểu
* có khả năng truy vết

---

## iii. bảng quyết định nhanh

| loại hệ thống                       | cần test       |
| ----------------------------------- | -------------- |
| có job / scheduler                  | 1–5 (bắt buộc) |
| có gọi hệ thống khác                | 1–5 (bắt buộc) |
| có retry / chạy lại                 | 1–5 (bắt buộc) |
| nhiều bước, song song               | 6–10 (nên có)  |
| liên quan tiền / dữ liệu quan trọng | 6–10 (rất nên) |

---

## iv. kết luận

* qc bảo vệ **đúng nghiệp vụ**
* dev bảo vệ **độ an toàn hệ thống**

checklist này không để test cho đủ.
nó để **đi trước sự cố một bước** và **không để production dạy mình bài học lúc nửa đêm**.

làm đúng 20/80:

* ít test hơn
* đúng chỗ hơn
* quyết định nhanh hơn
* hệ thống sống lâu hơn

---
