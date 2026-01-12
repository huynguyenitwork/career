# quyết định nhanh cho ý 5 & 6 (áp dụng cho mọi hệ thống)

## mục tiêu

- quyết định **có cần triển khai hay không**
- nếu theo **bdd** thì **viết thế nào**
- **test gì là đủ**
- **xử lý ra sao** khi tình huống xảy ra

---

## ý 5 – *có dữ liệu nhưng người dùng không thấy*

### có cần triển khai không?

**không bắt buộc**, nhưng **nên** nếu:

- service trả trạng thái cho ui
- có async / eventual consistency
- có sync nhiều hệ

**không cần** nếu:

- service chỉ là internal job, không ai phụ thuộc trạng thái
- không có ui hay hệ downstream đọc trạng thái

---

### theo bdd – viết ở mức tối thiểu

**feature:** trạng thái dữ liệu có thể hiển thị hay chưa

**scenario (cốt lõi):**

- given dữ liệu đã được đồng bộ kỹ thuật
- when nghiệp vụ chưa hoàn tất
- then trạng thái **chưa được coi là sẵn sàng cho người dùng**

→ chỉ cần **phân biệt được 2 trạng thái**:

- xong kỹ thuật
- xong để dùng

---

### test gì là đủ (20/80)

- service trả về **đúng trạng thái** theo từng bước
- không test ui
- không test render

chỉ test:

- trạng thái a → b có đúng không
- có trường hợp trả trạng thái “chưa sẵn sàng” không

---

### giải pháp khi xảy ra

- tách rõ:

  * `synced` (xong đồng bộ)
  * `ready` (có thể dùng)
- ui không cần suy luận
- không dùng 1 trạng thái chung kiểu `done`

---

## ý 6 – *mỗi hệ thống hiểu khác nhau cùng một khái niệm*

### có cần triển khai không?

**bắt buộc** nếu:

- có hơn 1 hệ đọc dữ liệu
- có integration / message / event
- có trạng thái dùng cho quyết định tiếp theo

**không triển khai = chấp nhận bug ngầm**

---

### theo bdd – viết ở mức tối thiểu

**feature:** trạng thái có ý nghĩa thống nhất giữa các hệ

**scenario (cốt lõi):**

- given service phát trạng thái x
- when hệ khác nhận trạng thái đó
- then hệ nhận **không cần suy đoán để xử lý tiếp**

bdd ở đây **không test ui**, mà test:

- trạng thái có đủ thông tin vận hành hay không

---

### test gì là đủ (20/80)

- contract test:

  * field có đủ không
  * ý nghĩa có rõ không
- không test logic nghiệp vụ của hệ nhận
- không test ui

chỉ test:

- hệ nhận **có thể quyết định tiếp hay dừng**

---

### giải pháp khi xảy ra

- định nghĩa trạng thái bằng **hành vi**, không bằng tên
- trạng thái phải trả lời được 3 câu:

  1. có retry không?
  2. có hiển thị được không?
  3. có cho phép bước tiếp theo không?

nếu trạng thái **không trả lời được 3 câu trên** → trạng thái đó **thiết kế chưa đạt**.

---

## bảng quyết định nhanh (đọc là chốt)

| ý   | có cần làm không | khi nào làm    | giá trị mang lại        |
| --- | ---------------- | -------------- | ----------------------- |
| ý 5 | nên              | có ui / async  | tránh user hiểu sai     |
| ý 6 | bắt buộc         | có integration | tránh hệ thống hiểu sai |

---

## kết luận ngắn gọn

- **ý 5**: không làm thì không chết ngay, nhưng dễ bị chửi
- **ý 6**: không làm thì sớm muộn cũng vỡ

nếu bạn chỉ chọn **1 trong 2 để làm trước** → **làm ý 6 trước**, vì:

> hệ thống chịu được ui xấu,
> nhưng **không chịu được hiểu sai dữ liệu**.

nếu muốn, mình có thể **viết luôn template bdd + checklist test** để bạn copy dùng cho mọi service.
