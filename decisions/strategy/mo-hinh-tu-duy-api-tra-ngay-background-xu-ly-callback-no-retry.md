## mô hình tư duy: api trả ngay + background xử lý + callback (no retry)

---

## mục tiêu thiết kế (giữ cái ảnh hưởng quyết định)

- api trả ngay, không block
- client nhận trạng thái duy nhất: "queued"
- xử lý nặng chạy sau
- callback báo kết quả cuối
- không retry trong service này

---

## nguyên lý cốt lõi (đinh)

- api ≠ hoàn tất nghiệp vụ
- api chỉ làm 2 việc:
  - validate đầu vào
  - ghi nhận yêu cầu xử lý
- background chịu toàn bộ nghiệp vụ
- callback là tín hiệu kết thúc

=> tách request lifecycle khỏi business lifecycle  
=> tách được thì hệ thống thở được

---

## tư duy luồng xử lý (rút gọn)

- client gọi
- api validate
- api enqueue
- api trả ngay
- background xử lý
- background callback

kết luận:
- api chết sau khi enqueue → vẫn ổn
- giá trị nằm ở việc "đã ghi nhận", không phải "đã xong"

---

## vai trò controller (chỉ làm đúng phần mình)

- kết thúc nhanh
- không chờ xử lý thật
- không ôm try/catch nghiệp vụ
- không quyết định kết quả cuối

controller = cổng ghi nhận, không phải não xử lý

---

## tư duy về queue (20/80)

- chỉ cần:
  - nhận job
  - đẩy cho background xử lý ngay
- không cần:
  - retry
  - persistence
  - dead letter
  - survive restart

lý do:
- không retry → không cần lưu
- job mất = chấp nhận được
- yêu cầu duy nhất: chạy ngay khi có

---

## tư duy background service

- đây là nơi duy nhất làm nghiệp vụ
- try/catch dùng để:
  - xác định kết quả
  - không dùng để cứu vãn
- success hay fail đều là kết quả hợp lệ

nguyên tắc:
- thất bại không phải bug
- thất bại là trạng thái cần được báo ra

---

## tư duy callback

- callback là tín hiệu, không phải giao dịch
- gửi một chiều
- không chờ phản hồi
- không retry

ý nghĩa:
- callback chỉ nói: "ta đã xử lý xong"
- không đòi cam kết phía nhận

---

## ranh giới thiết kế (để không vượt)

mô hình này sai khi bạn cần:

- job không được mất
- retry nội bộ
- nhiều instance cùng xử lý queue
- delayed / scheduled job

nếu chưa có yêu cầu trên → loại ngay

---

## quyết định nâng cấp (filter nhanh)

- chưa đau vì mất job → chưa cần bền
- chưa cần retry → đừng thêm
- chưa scale multi-node → đừng phân tán
- chưa có sla cứng → đừng phức tạp

nâng cấp sớm = tự gài bẫy mình

---

## câu chốt để nhớ

- api trả nhanh để sống
- background làm chậm để đúng
- callback nói thật để khép vòng