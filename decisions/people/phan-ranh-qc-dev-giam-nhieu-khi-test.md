# phân ranh qc / dev — khung giảm nhiễu khi test

## mục tiêu
- giữ đúng ranh giới vai trò qc / dev
- giảm rủi ro hệ thống mà không giẫm việc nhau

## không phải
- không tranh luận đúng sai
- không test chồng chéo
- không ôm trách nhiệm hộ nhau

---

## nguyên tắc nhớ nhanh
- qc lo "đúng với người dùng"
- dev lo "hệ thống không tự làm bậy"

---

## phần của qc — dev loại
- kiểm tra luồng người dùng
- kiểm tra yêu cầu nghiệp vụ
- kiểm tra hiển thị và kết quả

tiêu chí nhận diện:
- người dùng có thấy đúng không?
- hành vi có đúng mô tả không?

kết luận:
- qc đảm bảo "làm đúng cái cần làm"
- dev không test lại phần này

---

## phần của dev — cần chủ động
- kiểm tra dữ liệu sai / thiếu
- kiểm tra hệ thống phụ không phản hồi
- kiểm tra chạy lại, retry, double action

tiêu chí nhận diện:
- nếu mọi thứ không hoàn hảo thì sao?
- hệ thống có tự gây lỗi không?

kết luận:
- dev đảm bảo "không làm sai khi điều kiện xấu"

---

## cách phân ranh trong 5 giây
- câu hỏi về cảm nhận / kết quả người dùng → qc
- câu hỏi về hành vi hệ thống khi lệch chuẩn → dev

---

## lý do dev phải test case "lệch"
- dữ liệu thực tế hay thiếu
- hệ thống hay trễ / fail
- production hiếm khi giống tài liệu

thực tế:
- phần lớn sự cố đến từ tình huống ít ai nghĩ tới

---

## cách nói để không giẫm vai
- "case này em test để giảm rủi ro hệ thống, không liên quan nghiệp vụ."
- "luồng này qc cover rồi, em không test lại."

---

## kết luận
- qc giữ sản phẩm đúng và đẹp
- dev giữ hệ thống không chết và không làm bậy
- mục tiêu chung: khách hàng không phải người đầu tiên thấy lỗi
