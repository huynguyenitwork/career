# luồng xử lý giao dịch mua bán getsaletransactions – bản quyết định nhanh

## 1. mục tiêu hàm
- nhận 1 yêu cầu sale (store / shift / bill / server)
- trả về 1 gói duy nhất đủ dữ liệu để export xml
- thiếu dữ liệu → coi như thất bại

## 2. khóa input ngay đầu hàm
- store id → thiếu → dừng
- shift id hoặc bill id → thiếu → dừng
- server context → thiếu → dừng
- input không xác định rõ → không chạy

## 3. chiến lược lấy dữ liệu
- tất cả query chạy song song → chậm → thất bại thiết kế
- mỗi loại dữ liệu = 1 nguồn riêng
- không phụ thuộc thứ tự → chỉ cần đủ

## 4. danh sách dữ liệu bắt buộc phải gom
- idocheader → thiếu → không export
- transaction (bill gốc) → thiếu → dừng
- transactionex → thiếu → chấp nhận nếu optional
- lineitem → thiếu → dừng
- lineitemex → thiếu → chấp nhận nếu optional
- lineitemdisc → không có → coi như 0
- lineitemtax → không có → coi như 0
- payment → thiếu → dừng
- creditcard → chỉ lấy khi payment = card

## 5. điểm đồng bộ sống còn
- chỉ đóng gói khi tất cả query trả về
- có query fail → fail toàn bộ
- không cho trả gói sale data thiếu phần cốt lõi

## 6. cấu trúc output cố định
- saledata gồm:
  - idocheader
  - transaction
  - transactionex
  - lineitem
  - lineitemex
  - lineitemdisc
  - lineitemtax
  - payment
  - creditcard
- thêm field mới → phải cập nhật exporter xml

## 7. nguyên tắc xử lý lỗi
- sp nào lỗi → log rõ sp đó
- không swallow exception
- không tự suy đoán dữ liệu thay thế

## 8. công thức rà soát 5 phút
- input đã khóa chưa?
- có chạy song song không?
- thiếu phần nào là fail?
- output có đủ để export xml không?
- thêm dữ liệu mới có phá xml không?

## 9. nhiễu cần loại
- giải thích nghiệp vụ dài dòng
- query không dùng cho export
- dữ liệu không ảnh hưởng 7–30 ngày
- logic "cho có dữ liệu tạm"
