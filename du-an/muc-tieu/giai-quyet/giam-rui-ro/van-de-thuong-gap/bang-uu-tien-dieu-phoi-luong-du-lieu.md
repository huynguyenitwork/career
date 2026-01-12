# bảng ưu tiên điều phối

## kỹ thuật ↔ thực tế

*(queue / retry / monitoring / auto-healing)*

---

## ưu tiên 1 — **bắt buộc, làm trước**

> *thiếu là hệ thống sai, đừng bàn tiếp*

| quyết định            | kỹ thuật        | thực tế                   | hành động           |
| --------------------- | --------------- | ------------------------- | ------------------- |
| có việc rõ ràng       | job = 1 entity  | 1 đơn = 1 kiện            | tách job            |
| có trạng thái         | status trong db | đơn có trạng thái         | lưu db              |
| không trùng           | idempotent      | giao lại không giao trùng | requestkey          |
| thứ tự ở logic        | condition check | có hàng mới giao          | check trong handler |
| worker chết không sao | stateless       | shipper nghỉ vẫn giao     | không giữ state     |

**→ xong ưu tiên 1 thì hệ thống mới “đúng”.**

---

## ưu tiên 2 — **làm ngay để đỡ mệt**

> *thiếu vẫn chạy, nhưng vận hành khổ*

| quyết định         | kỹ thuật               | thực tế         | hành động  |
| ------------------ | ---------------------- | --------------- | ---------- |
| lỗi tạm            | retry giới hạn         | giao lại x lần  | retrycount |
| chạy nhanh         | song song có kiểm soát | nhiều shipper   | n worker   |
| không xử trùng     | lock db                | 1 đơn 1 shipper | trymark    |
| biết lúc can thiệp | monitoring 4 số        | nhìn kẹt đường  | dashboard  |

**→ xong ưu tiên 2 thì hệ thống “sống khỏe”.**

---

## ưu tiên 3 — **tùy chọn, để cuối**

> *không có vẫn ổn*

| quyết định   | kỹ thuật        | thực tế            | khi cần     |
| ------------ | --------------- | ------------------ | ----------- |
| giãn tải     | delay / backoff | tránh giờ cao điểm | rate limit  |
| ưu tiên      | priority        | đơn gấp            | backlog lớn |
| lưu job chết | dead letter     | kho hủy            | audit       |

**→ chỉ làm khi hệ thống đã ổn.**

---

## bảng quyết nhanh (nhìn là chọn)

| câu hỏi                     | có              | không          |
| --------------------------- | --------------- | -------------- |
| có phụ thuộc kết quả trước? | check điều kiện | song song      |
| sai có sửa được?            | retry           | fail vĩnh viễn |
| worker chết có sao?         | ok              | sai thiết kế   |
| cần giãn tải?               | delay           | không timing   |
| retry chạm trần?            | con người       | để hệ thống    |

---

## 3 câu “khóa não” (đủ dùng)

1. **queue không tạo thứ tự, chỉ giữ việc.**
2. **thứ tự nằm trong điều kiện, không nằm trong thời gian.**
3. **cái bắt buộc làm trước để không sai; tối ưu làm sau.**