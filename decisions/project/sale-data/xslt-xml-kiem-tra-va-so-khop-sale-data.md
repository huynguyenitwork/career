# xslt → xml: kiểm tra và so khớp sale data (bản nén)

## phạm vi
- chỉ dùng để phát hiện sai/thiếu giữa xml export và sale data chuẩn
- không bàn lý thuyết xslt, không hướng dẫn code

---

## mục tiêu quyết định
- xác định nhanh xml hiện tại **đạt / không đạt chuẩn sale data**
- chỉ ra **field/segment cần sửa** để gửi hệ thống nhận

---

## đầu vào bắt buộc
- xml export hiện tại
- tài liệu sale data chuẩn (segment, field, kiểu, thứ tự)
- file xslt đang dùng (nếu có)

thiếu 1 trong 3 → dừng

---

## đầu ra cần có
- danh sách gap:
  - thiếu segment
  - sai tên field
  - sai kiểu dữ liệu
  - sai thứ tự
- xml đã chỉnh, chạy hợp lệ

không ra được 2 thứ này → thất bại

---

## nguyên tắc lọc
- không đọc xml bằng mắt
- không so từng dòng
- chỉ dựa trên **kết quả chạy xslt + lỗi báo**

---

## luồng 20/80
- chạy xslt với xml hiện tại
- có output → mapping cơ bản đúng
- output trống hoặc error → xác định sai ngay tại:
  - tag name
  - xpath
  - cấp cha
  - field thiếu

---

## checklist tối thiểu
- xslt có chạy không?
- các group chính có output không:
  - saletotal
  - paymenttotal
  - disctotal
  - taxtotal
  - sale / lineitem
- lỗi báo chỉ ra field nào?

check không qua → quay lại sửa mapping

---

## hành động sửa
- thiếu dữ liệu → sửa nguồn
- sai mapping → sửa xslt
- sai định nghĩa → cập nhật theo sale data chuẩn

chỉ sửa đúng chỗ bị báo lỗi, không mở rộng

---

## công cụ đủ dùng
- xslt tester (linangdata)
- testxslt (easycodeforall)

chạy được + thấy lỗi rõ → đạt

---

## kết luận vận hành
- chạy xslt là phép thử duy nhất cần làm
- lỗi = chỉ dẫn sửa
- không cần excel, không cần so tay
- xml chạy ra hợp lệ = đủ điều kiện gửi hệ thống nhận