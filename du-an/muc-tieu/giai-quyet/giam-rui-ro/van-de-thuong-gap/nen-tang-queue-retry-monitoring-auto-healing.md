# queue / retry / monitoring / auto-healing

mục tiêu: điều phối và phân luồng phù hợp với hệ thống

## so sánh kỹ thuật ↔ đời thực (giao thông / giao hàng)

---

## 1. queue là gì?

| kỹ thuật              | đời thực                     |
| --------------------- | ---------------------------- |
| bảng lưu job trong db | trung tâm điều phối đơn hàng |
| job nằm chờ `pending` | đơn nằm trong kho            |
| worker quét job       | shipper tới kho nhận đơn     |

**tinh thần chung**
không ai xếp hàng đứng chờ.
ai **tới đúng lúc – đủ điều kiện** thì lấy việc làm.

---

## 2. pending / processing / done / failed

| kỹ thuật   | đời thực                    |
| ---------- | --------------------------- |
| pending    | đơn đã tạo, chưa giao       |
| processing | shipper đang cầm hàng       |
| done       | giao xong                   |
| failed     | giao không được, trả về kho |

**tinh thần chung**
trạng thái để **biết chuyện gì đang xảy ra**,
không phải để chờ đợi nhau.

---

## 3. worker vận hành thế nào?

| kỹ thuật                   | đời thực                        |
| -------------------------- | ------------------------------- |
| worker không biết bối cảnh | shipper không biết đơn khác     |
| nhặt job đủ điều kiện      | lấy đơn giao được               |
| xử xong thì báo trạng thái | giao xong thì cập nhật hệ thống |

**tinh thần chung**
mỗi người **lo việc của mình**,
điều phối nằm ở trung tâm.

---

## 4. thứ tự xử lý nằm ở đâu?

| kỹ thuật                      | đời thực                   |
| ----------------------------- | -------------------------- |
| check điều kiện trong handler | kiểm tra hàng có trong kho |
| không chờ job khác            | không đứng đợi xe khác     |
| fail nếu chưa đủ              | không xuất kho nếu thiếu   |

**tinh thần chung**
thứ tự là **luật**,
không phải **đồng hồ**.

---

## 5. khi nào cần tuần tự (step-by-step)?

| kỹ thuật                      | đời thực                 |
| ----------------------------- | ------------------------ |
| job sau cần kết quả job trước | chưa nhập kho không giao |
| không retry được              | hàng vỡ là xong          |
| side-effect nguy hiểm         | giao nhầm là mất         |

**tinh thần chung**
có **rủi ro không quay đầu** → đi chậm.

---

## 6. khi nào chạy song song / đồng thời?

| kỹ thuật               | đời thực            |
| ---------------------- | ------------------- |
| job độc lập            | nhiều đơn khác nhau |
| retry an toàn          | giao lại được       |
| không đụng cùng entity | không chung địa chỉ |

**tinh thần chung**
không rủi ro → **đi đông cho nhanh**.

---

## 7. retry là gì?

| kỹ thuật             | đời thực             |
| -------------------- | -------------------- |
| job failed còn retry | giao không gặp khách |
| retrycount           | số lần quay lại      |
| maxretry             | quá số lần thì dừng  |

**tinh thần chung**
không giao được **không có nghĩa là sai**,
có thể là **chưa tới lúc**.

---

## 8. timing / delay dùng khi nào?

| kỹ thuật      | đời thực                |
| ------------- | ----------------------- |
| backoff retry | hẹn giao lại buổi chiều |
| rate limit    | giờ cao điểm            |
| nextretryat   | đặt lịch quay lại       |

**tinh thần chung**
không phải lúc nào cũng lao vào,
đôi khi **đợi đúng thời điểm** mới là nhanh.

---

## 9. monitoring nhìn cái gì?

| kỹ thuật       | đời thực              |
| -------------- | --------------------- |
| pending tăng   | đơn tồn kho           |
| processing lâu | shipper mất tích      |
| failed nhiều   | tuyến đường có vấn đề |
| retry tăng đều | khu vực đang khó giao |

**tinh thần chung**
không soi từng bánh xe,
chỉ nhìn **tắc đường – tai nạn – ùn đơn**.

---

## 10. auto-healing là gì?

| kỹ thuật         | đời thực                       |
| ---------------- | ------------------------------ |
| worker restart   | shipper nghỉ → người khác giao |
| job còn trong db | đơn vẫn nằm ở kho              |
| retry tự chạy    | giao lại hôm sau               |

**tinh thần chung**
hệ thống **không cần anh hùng**,
chỉ cần **không quên việc**.

---

## 11. bảng quyết nhanh (kỹ thuật ↔ đời thực)

| câu hỏi                   | kỹ thuật        | đời thực           |
| ------------------------- | --------------- | ------------------ |
| có phụ thuộc trước không? | check điều kiện | có hàng chưa?      |
| sai có quay lại được?     | retry           | giao lại           |
| không quay lại được?      | dừng            | hàng hỏng          |
| độc lập?                  | song song       | nhiều shipper      |
| cần giãn tải?             | delay           | tránh giờ cao điểm |

---

## 12. một câu chốt cho cả hai thế giới

> queue giống giao thông:
> luật nằm ở điều kiện,
> tốc độ nằm ở số người,
> hồi phục nằm ở việc **không quên**.

nếu bạn nói chuyện với:

* **kỹ thuật** → dùng cột trái
* **po / vận hành** → dùng cột phải

hai bên sẽ **hiểu cùng một thứ**, chỉ khác ngôn ngữ.

nếu cần, bước tiếp theo rất hợp lý là:

* 1 sơ đồ “từ kho → giao → hoàn”
* hoặc 1 slide duy nhất cho họp quyết định

nhưng về **hiểu để điều phối đúng**, bảng này là đủ khóa não rồi.
