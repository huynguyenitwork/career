# restful api – cơ chế cốt lõi và cách dùng đúng

## mục tiêu
- thống nhất nhận thức khi thiết kế và sử dụng restful api, tránh hiểu sai cơ chế dẫn đến mất dữ liệu, hành vi mơ hồ hoặc nợ kỹ thuật.
- trọng tâm là **trách nhiệm của từng http method** và **cách dùng put đúng bản chất**, kèm happy path và edge case.

---

## 1. triết lý nền

restful api không xoay quanh việc "gọi cho chạy", mà là **hợp đồng trạng thái giữa client và server**.

- client mô tả **điều mình muốn xảy ra**
- server chịu trách nhiệm **đưa hệ thống về trạng thái tương ứng**
- mỗi http method mang một ý nghĩa ngữ nghĩa rõ ràng

hiểu sai method = phá hợp đồng.

---

## 2. get – đọc trạng thái, tuyệt đối không gây side effect

### cơ chế cốt lõi

get dùng để **truy xuất trạng thái hiện tại của resource**.

- chỉ đọc
- không tạo
- không cập nhật
- không xóa

### đặc tính

- safe: không làm thay đổi hệ thống
- idempotent: gọi nhiều lần kết quả không đổi
- cacheable

### dùng đúng khi

- lấy danh sách
- lấy chi tiết
- kiểm tra trạng thái

### dùng sai khi

- get nhưng lại cập nhật dữ liệu (ví dụ đánh dấu đã xem)
- get nhưng sinh nghiệp vụ quan trọng

---

## 3. post – tạo mới hoặc kích hoạt hành động

### cơ chế cốt lõi

post dùng khi **server cần tạo ra một điều mới** hoặc **thực hiện một hành động có side effect**.

### đặc tính

- không idempotent
- server quyết định kết quả cuối

### dùng đúng khi

- tạo entity mới
- submit form
- trigger process (approve, gửi email, import, tính toán)

### dùng sai khi

- dùng post để update chỉ vì tiện
- mong post an toàn khi retry

---

## 4. put – thay thế toàn bộ resource

### cơ chế cốt lõi

put dùng để **replace hoàn toàn resource hiện tại bằng trạng thái mới**.

nói cách khác:

> sau khi put xong, resource phải giống hệt payload được gửi lên.

### đặc tính

- idempotent
- mang tính đồng bộ trạng thái

### hệ quả quan trọng

- field không gửi → coi như không tồn tại
- null khác với không truyền

### dùng đúng khi

- update form đầy đủ
- sync dữ liệu giữa các hệ thống
- client nắm toàn bộ trạng thái entity

### dùng sai khi

- chỉ gửi vài field nhưng mong field khác giữ nguyên
- dùng put như patch

---

## 5. patch – cập nhật từng phần

### cơ chế cốt lõi

patch dùng để **thay đổi một phần resource mà không đụng tới phần còn lại**.

### đặc tính

- không replace toàn bộ
- server phải merge dữ liệu

### dùng đúng khi

- chỉnh sửa một vài thuộc tính
- user update profile từng phần

### lưu ý

- patch phức tạp hơn put
- cần định nghĩa rõ rule merge

---

## 6. delete – loại bỏ resource

### cơ chế cốt lõi

delete dùng để **loại resource khỏi hệ thống** (vật lý hoặc logic).

### đặc tính

- idempotent
- không cần body

### lưu ý

- soft delete vẫn là delete về mặt api contract

---

## 7. tổng hợp nhanh

- get: đọc
- post: tạo / hành động
- put: thay thế toàn bộ
- patch: cập nhật từng phần
- delete: xóa

---

# phần 2 – case cụ thể: put api

## 8. bối cảnh

api cập nhật entity sử dụng put.
request yêu cầu gần như đầy đủ các field của entity.

hành vi:

- field không truyền hoặc truyền null → giá trị trong db bị set null.

đây là **đúng bản chất put**, không phải bug.

---

## 9. happy path – dùng put đúng

### điều kiện

- client nắm toàn bộ trạng thái entity
- client gửi payload đầy đủ

### luồng

1. client lấy entity hiện tại bằng get
2. client chỉnh sửa dữ liệu
3. client gửi put với đầy đủ field
4. server replace entity

### kết quả

- dữ liệu nhất quán
- không mất field ngoài ý muốn
- retry an toàn

---

## 10. edge case – dùng put sai hoặc nguy hiểm

### case 1: client chỉ gửi một vài field

- nguyên nhân: hiểu put như update từng phần
- hậu quả: các field không gửi bị set null
- bản chất: put đang làm đúng, client dùng sai

### case 2: client quên field vì version mismatch

- client cũ không biết field mới
- gửi put → field mới bị xóa
- đây là rủi ro lớn của put nếu không quản lý version

### case 3: backend cố tình merge ngầm

- put nhưng server giữ lại field cũ
- hành vi giống patch
- hậu quả:

  * mơ hồ contract
  * khó debug
  * nợ kỹ thuật

---

## 11. nguyên tắc chọn put hay patch

- client nắm toàn bộ entity → put
- client chỉ chỉnh một phần → patch
- không chắc client có đủ dữ liệu → patch

---

## 12. câu kết

put không phải update nhẹ.
put là tuyên bố trạng thái mới của resource.

thiết kế đúng http method không phải vấn đề hình thức, mà là cách bảo vệ dữ liệu, giảm bug và giữ hệ thống có kỷ luật về lâu dài.
