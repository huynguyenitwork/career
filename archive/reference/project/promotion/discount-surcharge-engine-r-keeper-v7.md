# discount / surcharge engine – r-keeper v7  

---

## mục tiêu
- coi discount là **pricing rule engine**, không phải phép cộng
- xác định đúng **điểm gây lệch tiền** khi sync / debug
- mỗi mục = 1 gate logic, sai gate = sai tiền

---

## 1. bản chất hệ thống
- discount / surcharge = rule engine có trạng thái
- gồm: rule, điều kiện, priority, scope, composition
- kết luận: không được map như field cộng thêm
- dùng để làm gì: tránh thiết kế sync sai ngay từ đầu

---

## 2. discount entity
- giá trị: % hoặc số tiền
- loại: giảm hoặc phụ thu
- không có detail → không hoạt động
- dùng để làm gì: chỉ là **vỏ**, không có logic

---

## 3. detail (rule thực thi)
- mỗi discount có ≥1 detail
- detail gồm: value, condition, priority
- duyệt theo priority
- gặp detail đầu tiên thỏa → áp dụng
- % discount có thể áp dụng trên nhiều item
- kết luận: **short-circuit rule evaluation**
- dùng để làm gì: xác định discount chạy hay không

---

## 4. scope (phạm vi)
- order: toàn đơn, chỉ 1 instance
- seat / guest: theo từng khách
- item: theo từng dòng item
- sai scope → sai toàn bộ tiền
- dùng để làm gì: map đúng phạm vi khi sync

---

## 5. distributed flag
- distributed:
  - phân bổ vào item
  - tổng đúng, item thay đổi
- non-distributed:
  - tạo dòng riêng
  - có thể không tax, không fiscal
  - không bị discount khác tác động
- ví dụ: tip, service fee
- kết luận: non-distributed ≠ item bán hàng
- dùng để làm gì: tránh lệch báo cáo

---

## 6. composition (kết hợp)
- freely combinable → luôn cộng
- non-combinable → bắt buộc có composition
- kiểu composition:
  - cộng
  - lấy lớn nhất
  - lấy cái đầu
  - giảm dần
- không có composition hợp lệ → discount bị loại
- chỉ áp dụng trên **vùng scope giao nhau**
- dùng để làm gì: xử lý 80% case “không ra tiền”

---

## 7. usage rule (auto vs manual)
- allow / deny / automatic
- automatic:
  - không sửa giá trị
  - có thể bị xóa nếu có quyền
  - nhiều auto → lấy code nhỏ hơn
- automatic ≠ manual dù cùng code
- dùng để làm gì: tránh sync nhầm discount hệ thống

---

## 8. condition nâng cao trong detail
- phụ thuộc:
  - category
  - min amount / quantity
  - guest count / type
  - restaurant
  - bonus type (pds)
- flag quan trọng: apply on exceeding
  - chỉ áp dụng phần vượt ngưỡng
  - phụ thuộc thứ tự item
- kết luận: không thể tính lại chỉ từ tổng tiền
- dùng để làm gì: debug case lệch tiền khó

---

## 9. payment-level discount
- gắn với currency
- áp dụng khi thanh toán
- có thể auto
- không áp dụng lại nếu đã có manual cùng scope
- payment ≠ order
- có thể xuất hiện sau khi order đóng
- dùng để làm gì: debug lệch tiền lúc payment

---

## 10. tip / gratuity
- non-distributed surcharge
- có thể:
  - không fiscal
  - không tax
  - không qua detail rule
- có logic riêng khi change → tip
- cấm map tip thành item bán hàng
- dùng để làm gì: tránh sai sổ thuế / báo cáo

---

## checklist sync bắt buộc
- item line identity
- scope
- distributed flag
- applied discount list
- auto vs manual
- final value sau composition

---

## bản đồ debug nhanh
- không áp dụng → kiểm composition
- tổng đúng, item sai → kiểm distributed
- payment lệch → kiểm payment discount
- tip lệch → kiểm non-fiscal

---

## kết luận
- đây là **pricing rule engine có priority + scope + state**
- nhớ 5 từ khóa là đủ an toàn:
  "rule" – "detail" – "scope" – "composition" – "distribution"
