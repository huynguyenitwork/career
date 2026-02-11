# các case bdd rủi ro hệ thống thường gặp

## mục tiêu
- nhận diện nhanh nguyên nhân gốc gây lỗi production
- dùng để soi edge case, không dùng để test nghiệp vụ
- áp dụng cho ui, api, async, job, multi-system

## không phải
- không liệt kê cho đủ
- không phân tích dài
- không suy đoán ngoài hệ thống

---

## case 1 — một hành động bị xử lý nhiều lần

### dấu hiệu
- cùng một ý định nhưng hệ thống xử lý lặp

### nguyên nhân cần check
- ui không disable / không feedback → user bấm lại
- client retry nhưng không có định danh
- backend không idempotent
- async trả kết quả trễ, client hành động thêm

### tiêu chí loại
- một request = một hiệu ứng duy nhất
- không phân biệt được cùng ý định → rủi ro cao

---

## case 2 — việc sau chạy khi việc trước chưa xong

### dấu hiệu
- thứ tự xử lý sai, trạng thái lệch

### nguyên nhân cần check
- thiếu ràng buộc thứ tự
- không lưu trạng thái trung gian
- event đến nhanh hơn khả năng xử lý
- giả định ngầm “chắc xong rồi”

### tiêu chí loại
- business cần tuần tự nhưng hệ thống cho song song

---

## case 3 — gửi tới đối tượng không còn hợp lệ

### dấu hiệu
- xử lý trễ, fail muộn, khó trace

### nguyên nhân cần check
- cache lỗi thời
- không validate trạng thái trước khi gửi
- async job chạy trễ không re-check
- receiver không reject rõ ràng

### tiêu chí loại
- chỉ cần id là xử lý → rủi ro cao

---

## case 4 — giao rồi nhưng không ai xác nhận (ack)

### dấu hiệu
- sender không biết đã xong hay chưa

### nguyên nhân cần check
- không implement ack
- ack gửi sai nơi
- ack gửi nhưng sender không nhận
- ack thiếu hoặc sai định danh
- ack không idempotent
- ack phụ thuộc vào luồng bất định
- không thống nhất định nghĩa “thành công”

### tiêu chí loại
- http 200 nhưng chưa rõ trạng thái thực → loại

---

## case 5 — có dữ liệu nhưng người dùng không thấy

### dấu hiệu
- hệ thống có data nhưng ui trống

### nguyên nhân cần check
- query sai
- cache / index chưa cập nhật
- phân quyền hiển thị không khớp
- ui không refresh theo thay đổi

### tiêu chí loại
- data đúng nhưng không truy xuất đúng

---

## case 6 — cùng khái niệm, mỗi hệ thống hiểu khác

### dấu hiệu
- ghép hệ thống thì lỗi, test riêng thì pass

### nguyên nhân cần check
- cùng field, khác semantics
- thiếu contract business
- thay đổi một phía không báo
- thiếu test end-to-end

### tiêu chí loại
- chỉ thống nhất schema, không thống nhất ý nghĩa

---

## kết luận
- phần lớn sự cố đến từ lệch trạng thái, lệch thời điểm, lệch khái niệm
- dev cần soi:
  - một hành động có bị xử lý nhiều lần không
  - thứ tự có bị phá không
  - đối tượng còn hợp lệ không
  - trạng thái có được xác nhận rõ không
  - các hệ thống có hiểu cùng một ý không

mục tiêu cuối:
- hệ thống không làm bậy khi đời không hoàn hảo
